import discord
from discord.ext import commands
import json
import os
from discord.utils import get
from discord import Member
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

import asyncio
from Pixiv.author import Pixiv



with open('./QQ.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix='!')

slash = SlashCommand(bot,sync_on_cog_reload=True, override_type=True   )#sync_on_cog_reload=True, override_type=True


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd,activity=discord.Game('期間限定QQ'))
    print(">> QQBot is online 0.< <<")
    


@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'QQ_cmds.{extension}')
    await ctx.send(f'Loaded {extension} done.')

@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'QQ_cmds.{extension}')
    await ctx.send(f'Un - Loaded {extension} done.')  

@bot.command()
async def reload(ctx,extension):
    bot.reload_extension(f'QQ_cmds.{extension}')
    await ctx.send(f'Re - Loaded {extension} done.') 

@bot.command(pass_context=True, name='status')
async def status(ctx, member: Member):
    await ctx.send(str(member.status))
#確認status ，用法:!status 暱稱

# @bot.command()
# async def download_image(
#     source_url: str, target_url: str, image_name: str = "") -> bool:  # 因為discord_bot規定要用非同步，所以一定要用async
#     result = False  # 回傳結果用，判斷是否下載成功
#     async with aiohttp.ClientSession() as session:  # aiohttp是一個類似requests的套件，只是他支援asyncio，不用這個非同步bot會有問題
#         async with session.get(source_url) as response:  # aiohttp就必須用這個格式來進行請求，有興趣了解再去看aiohttp是啥吧
#             if response.status == 200:  # 檢查回傳是成功的
#                 _image_name = (image_name if image_name else os.path.basename(urlparse(target_url).path)  # 從url抓出原始檔案名稱
#                 )  # 這邊算是一個檢查，如果你不給image_name，那就自動抓url附的檔案名稱
#                 with open(os.path.join(target_url, _image_name), "wb") as file:  # 建立一個空白檔案
#                     file.write(await response.read())  # 將你從url拿到的圖片資訊，寫進去檔案裡面
#                 result = True
#     return result






if __name__ == "__main__":
    for filename in os.listdir('./QQ_cmds'):
        if filename.endswith('.py'):
            bot.load_extension(f'QQ_cmds.{filename[:-3]}')
    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    bot.run(jdata['TOKEN'])

#如何打開setting.json(vscode的):ctrl+shift+p 搜尋setting 選擇開啟設定(JSON) (非工作區設定)