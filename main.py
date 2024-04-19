import asyncio
import random
import nest_asyncio

from app.live import BiliLive
import config


nest_asyncio.apply()


async def main():
    for user in config.USERS:
        async with BiliLive(user['SESSDATA'], user['BILI_JCT'], user['UID']) as l:
            medal = await l.get_fans_medal()

            medal_list = [*medal['data']['list'],
                          *medal['data']['special_list']]

            for item in medal_list:
                roomid, target_name, target_uid = item['room_info']['room_id'], item[
                    'anchor_info']['nick_name'], item['medal']['target_id']

                if 'UID_WHITE_LIST' not in user:
                    continue

                if str(target_uid) in map(str, user['UID_WHITE_LIST']):
                    print(f'checking {target_name}(ROOM_ID:{roomid})')

                    # 点赞 + 一个弹幕
                    print(await l.like_report(roomid, target_uid))
                    print(await l.send_danmaku(roomid, random.choice(config.MSG_LIST)))
                else:
                    print(
                        f'UID:{target_uid} {target_name} not in whitelist, skip it.')

if __name__ == '__main__':
    asyncio.run(main())
