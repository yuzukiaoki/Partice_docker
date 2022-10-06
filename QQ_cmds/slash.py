from typing import Optional
import discord, json, random
from discord.ext import commands
from discord import guild
from discord_slash import SlashCommand, SlashContext,cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from core.classes import Cog_Extension
from discord.ext.commands.errors import MissingPermissions
from discord_slash.utils import manage_commands

with open('QQ.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class bang(Cog_Extension):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    # 參考 https://morioh.com/p/bb2c6d3b1581  discord slash 使用class的方式
    # global commands are created by not including the scope argument into the @bot.command decorator. 
    # They will appear in all guilds your Bot is in. This process can take up to one hour to be completed on all guilds.
    # If you want to register your slash command globally, remove guild_ids parameter and wait 12 hours to let discord register your slash command globally.
    server  = [672378454750134272]
    @cog_ext.cog_slash(name="test",description="995阿99599595959595959", guild_ids=server)
    async def _test(self, ctx: SlashContext):
        embed = discord.Embed(title="embed test")
        await ctx.send(content="7777777777777諾克薩斯斷頭台", embeds=[embed])
    


    @cog_ext.cog_slash(name="test_two",description="騙人的吧7777777777   ???????????")
    async def _bird_bird(self, ctx: SlashContext):
        embed = discord.Embed(title="embed test")
        await ctx.send(content=random.choice(jdata['bird']))
    
    @cog_ext.cog_slash(name="thisFive",description="78787878")
    @commands.has_permissions(manage_messages=True)
    async def _thisFive(self, ctx: SlashContext):
        
        await ctx.send(content="9899999999999999諾克薩斯斷頭台")
    
    @_thisFive.error
    async def __thisFiveerror(self, ctx , error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("您沒有權限喔")

    @cog_ext.cog_slash(
        name="secretCommand", #不能有空白
        description="你說...甚麼",
        guild_ids=server,
        options=[
            create_option(
                name="option", #不能變名稱
                description="選一個",
                required=True,
                option_type=3, #這到底是啥
                choices=[
                    create_choice(
                        name="這是甚麼",
                        value="我　要　死　了",
                    ),
                    create_choice(
                        name="Any Idea?", #可以有空白
                        value="https://tenor.com/view/%E5%AD%94%E6%98%8E%E8%88%9E01-gif-25360801",
                    ),
                ]
            )
        ])
    async def _slash_option(self, ctx: SlashContext, option:str):
        await ctx.send(option)

#     @cog_ext.cog_slash(name="space", description="Space your text", guild_ids=server,
#     options=[manage_commands.create_option( #create an arg
#     name = "text", #Name the arg as "text"
#     description = "The text to space", #Describe arg
#     option_type = 3, #option_type 3 is string
#     required = True, #Make arg required
#   )])
#     async def _space(ctx: SlashContext, sentence):
#         newword = "" #define new sentence
#         for char in sentence: #For each character in given sentence
#             newword = newword + char + "   " #Add to new sentence  with space
#         await ctx.send(content=newword) #send mew sentence
    @cog_ext.cog_slash(name="invites", description="Space your text", guild_ids=server,
    options = [
        create_option(
            name = "userr",
            description = "The user to space",
            required = True,
            option_type= 6
        )

    ]
    )
    async def _invites(self, ctx: SlashContext,user:Optional[discord.User]):
        await ctx.send(str(user))


def setup(bot):
    bot.add_cog(bang(bot))