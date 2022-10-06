import requests ,random
import sys,traceback,json,asyncio
from datetime import datetime as dt
from datetime import timedelta
from imgurpython import ImgurClient
from Pixiv.author import Pixiv

def set_timeznoe(timezone):
    utc_time = dt.utcnow()
    local_time = utc_time + timedelta(hours=timezone)
    return local_time

async def docker_task(bot):
    exec = False
    pix=Pixiv()
    await bot.wait_until_ready()  # 等待bot 啟動完畢
    while not bot.is_closed():  # 如果bot沒有關閉的話 就一直loop
        
        now_time = set_timeznoe(8).strftime('%H:%M')  # 原為datetime.datetime.now()
        # with open('mumi_setting.json', 'r', encoding='utf8') as jfile:
        #     jdata = json.load(jfile)
        dragon_channel = bot.get_channel(743370434048950272)#396383026533105685 主要聊天室
        #print("(39)恐龍報時頻道: ",self.channel)
        if exec == False:
            print("開始爬蟲")
            await pix.main(6662895,'N')
            exec = True
            print("pixiv爬蟲完成")
        print("still looping")
        await dragon_channel.send("hehe")
        await asyncio.sleep(30)

