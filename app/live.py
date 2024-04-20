import base64

import aiohttp

LIVE_API_SET = {
    'get_fans_medal': 'https://api.live.bilibili.com/xlive/app-ucenter/v1/fansMedal/panel',
    'send_danmaku': 'https://api.live.bilibili.com/msg/send',
    'like_report': 'https://api.live.bilibili.com/xlive/app-ucenter/v1/like_info_v3/like/likeReportV3',
    'heartbeat': 'https://live-trace.bilibili.com/xlive/rdata-interface/v1/heartbeat/webHeartBeat'
}


class BiliLive(object):
    def __init__(self, sessdata, bili_jct, uid) -> None:
        self.sessdata = sessdata
        self.bili_jct = bili_jct
        self.uid = uid

        self.session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.session.close()

    def _request(self, method, url, **kwargs):
        headers = kwargs.get('headers', {})

        if 'user-agent' not in headers:
            headers.update(
                {'user-agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'''})

        if 'cookie' not in headers:
            headers.update(
                {'cookie': f'SESSDATA={self.sessdata};bili_jct={self.bili_jct}'})

        kwargs.update({'headers': headers})

        return self.session.request(method, url, **kwargs)

    async def get_fans_medal(self, page=1, size=20):
        async with self._request('GET', LIVE_API_SET['get_fans_medal'], params={
            'page': page,
            'page_size': size
        }) as resp:
            return await resp.json()

    async def send_danmaku(self, room_id, msg: str = None):
        data = {
            "bubble": 0,
            "msg": msg,
            "color": 5816798,
            "mode": 1,
            "room_type": 0,
            "jumpfrom": 85001,
            "reply_mid": 0,
            "reply_attr": 0,
            "replay_dmid": "",
            "statistics": {
                "appId": 100,
                "platform": 5
            },
            "fontsize": 25,
            "rnd": 1713517086,
            "roomid": room_id,
            "csrf": self.bili_jct,
            "csrf_token": self.bili_jct
        }

        async with self._request('POST', LIVE_API_SET['send_danmaku'], data=data) as resp:
            return await resp.json()

    async def like_report(self, room_id, anchor_id, click_time: int = 300):
        data = {
            "click_time": click_time,
            "room_id": int(room_id),
            "uid": int(self.uid),
            "anchor_id": int(anchor_id),
            "csrf_token": self.bili_jct,
            "csrf": self.bili_jct,
            "visit_id": ""
        }

        print(data, )

        async with self._request('POST', LIVE_API_SET['like_report'], data=data) as resp:
            return await resp.json()

    async def heartbeat(self, room_id, interval=60):
        params = {
            'hb': base64.b64encode(f'{interval}|{room_id}|1|0'.encode()).decode(),
            'pf': 'web'
        }

        async with self._request('GET', LIVE_API_SET['heartbeat'], params=params) as resp:
            return resp
