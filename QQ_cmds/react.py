from core.classes import Cog_Extension
from discord.ext import commands
import asyncio




class React(Cog_Extension):
    
    @commands.command()
    async def quiz(self,ctx):
        await ctx.send("A, B or C")

        try:
            msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)

        except asyncio.TimeoutError:
            await ctx.send("You took to long...")

        else:
            if msg.content == "A":
                await ctx.send("Correct")
            elif msg.content == "B":
                await ctx.send("Wrong")
            elif msg.content == "C":
                await ctx.send("Wrong")
            else:
                await ctx.send("Huh?")
    
    pass





def setup(bot):
    bot.add_cog(React(bot))