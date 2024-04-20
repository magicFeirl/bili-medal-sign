import asyncio
import random
import nest_asyncio

from app.live import BiliLive
import config


nest_asyncio.apply()


async def create_live_task(user: dict):
    async def create_heartbeat_task(hb, roomid, uname, minutes=65):
        beat_count = 0

        while beat_count < minutes:
            beat_count += 1
            print(f'heartbeating {uname}(ROOMID: {roomid})...')
            await hb(roomid)
            await asyncio.sleep(60)

    heartbeat_tasks = []

    async with BiliLive(user['SESSDATA'], user['BILI_JCT'], user['UID']) as l:
        medal = await l.get_fans_medal()

        medal_list = [*medal['data']['list'],
                      *medal['data']['special_list']]

        for item in medal_list:
            roomid, target_name, target_uid = item['room_info']['room_id'], item[
                'anchor_info']['nick_name'], item['medal']['target_id']

            # 没有配置 UID 白名单，跳过打卡
            if 'UID_WHITE_LIST' not in user:
                # user['UID_WHITE_LIST'] = []
                continue

            # 并发心跳
            heartbeat_tasks.append(
                create_heartbeat_task(l.heartbeat, roomid, target_name))

            # 仅白名单用户的直播间发送一个弹幕 和 点赞
            if str(target_uid) in map(str, user['UID_WHITE_LIST']):
                print(f'checking {target_name}(ROOM_ID:{roomid})')

                print(await l.like_report(roomid, target_uid))
                print(await l.send_danmaku(roomid, random.choice(config.MSG_LIST)))
            else:
                print(
                    f'UID:{target_uid} {target_name} not in whitelist, skip it.')

        await asyncio.gather(*heartbeat_tasks)


async def main():
    live_task = []

    for user in config.USERS:
        live_task.append(create_live_task(user))
        # await asyncio.sleep(random.randint(5, 15))

    await asyncio.gather(*live_task)


if __name__ == '__main__':
    asyncio.run(main())
