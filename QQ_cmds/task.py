import random
import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import asyncio
import datetime
import datetime
#from _datetime import date
from datetime import date, tzinfo, timedelta, datetime, timezone
#from facebook_scraper import get_posts
from data_file.get_something import some_list,time_task
#from cmds.event import ComplexEncoder
from data_file.docker_util import docker_task



class Task(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
    #     self.bg_task2=self.bot.loop.create_task(self.time_task())
        #self.bot.loop.create_task(time_task(self.bot))
        self.bot.loop.create_task(docker_task(self.bot))
        # self.bot.loop.create_task(self.hehe())
        # self.bot.loop.create_task(self.task1())
        # self.bg_task2=self.bot.loop.create_task(self.task2())
        # self.bg_task3=self.bot.loop.create_task(self.task3())





def setup(bot):
    bot.add_cog(Task(bot))
