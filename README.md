## B站粉丝牌保活

### 功能

自动发送弹幕 + 点赞获取粉丝牌每日 200 活跃度低保

### 使用

1. 重命名 `config.example.py` 为 `config.py`
2. 根据 `config.py` 的示例修改参数（COOKIE、自己的UID、要自动打卡的用户的UID、弹幕消息）
3. 通过 crontab 或者其他定时任务定时触发脚本，建议一天最多触发一次