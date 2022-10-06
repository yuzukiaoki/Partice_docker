from asyncio.tasks import sleep
from urllib import response
import discord
from discord import player
from discord.ext import commands
import json
from core.classes import Cog_Extension
import random
import json,asyncio
import datetime
from datetime import tzinfo, timedelta, timezone
#from datetime import date #原本 from _datetime import date
import requests
from datetime import datetime as dt
from data_file.get_something import *
from functools import partial

with open('QQ.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        # elif isinstance(obj, date):
        #     return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class Event(Cog_Extension):
   
    def __init__(self, *args, **kwargs):  # 基本化自訂函式
        super().__init__(*args, **kwargs)
        


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == "🔫" and user != self.bot.user:
            await reaction.message.add_reaction("❓")
            await reaction.message.add_reaction("🔫")
            print(reaction.message.channel.id)
            print(user.id)
            
            #await reaction.message.channel.send(f"{user} reacted with {reaction.emoji}")
    
    #https://unicode.org/emoji/charts/full-emoji-list.html -> emoji list

    @commands.Cog.listener()
    async def on_message(self,msg):
        #self.error_channel = self.bot.get_channel(1014378434782306304)
        await self.replyBot(msg)

    async def replyBot(self,msg):
        
        if msg.content.startswith ('恐龍88') and msg.author != self.bot.user:
            random_dragon2 = random.choice(jdata['bird'])
            await msg.channel.send(random_dragon2)
            #await self.error_channel.send("<@268570448294445056>"+f" honkai scrape錯誤失敗次數已達87次")

        elif "@!268570448294445056" in msg.content and msg.author != self.bot.user :
            random_mumi_mention = random.choice(jdata['bird'])
            await msg.channel.send(random_mumi_mention)
        elif "@!743339674143031298" in msg.content and msg.author != self.bot.user :
            random_dragon_mention = random.choice(jdata['soldier'])
            await msg.channel.send(random_dragon_mention)
        elif "bangbang" in msg.content and msg.author != self.bot.user :
            myid = '<@268570448294445056>'
            print(msg.author.id)
            await msg.channel.send(f"{myid},哈哈")
        elif "<@268570448294445056>" in msg.content and msg.author != self.bot.user :
            await msg.channel.send("阿")
        elif "nani" in msg.content and msg.author != self.bot.user :
            await msg.add_reaction("🐕")
            await msg.add_reaction("🐈")
            await msg.add_reaction("❓")
            await msg.channel.send("你說什麼",reference = msg, mention_author = False)
        
        if msg.content.startswith('!gogo'):
            channel = msg.channel
            await channel.send('Send me that 👍 reaction, mate')

            def check(reaction, user):
                return user == msg.author and str(reaction.emoji) == '👍'

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await channel.send('👎')
            else:
                await channel.send('👍')

        if msg.reference and msg.author.id != self.bot.user: #只要有任何reply 這個 reference就會被觸發 # msg.author != self.bot 不管用
            # print(f'這是名字: {msg.author.name}')
            # print(f'這是內容: {msg.content}')
            first_msg = msg
            msg = await msg.channel.fetch_message(msg.reference.message_id)
            if msg.author.id == 828265295897821194:
                # print(f'這是MSG: {msg}')
                # print(first_msg.content)
                # print(first_msg.author)
                # print(self.bot.user)
                if "知道" in first_msg.content and first_msg.author != self.bot.user :
                    # print("got it")
                    await asyncio.sleep(5)
                    await first_msg.reply("<:ik:744944189359521802>", mention_author=True)
                else:
                    random_reply_dragon = random.choice(jdata['dragon_reply'])
                    await asyncio.sleep(5)
                    await first_msg.reply(random_reply_dragon, mention_author=False)



def setup(bot):
    bot.add_cog(Event(bot))