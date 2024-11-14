import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if "comkean" in message.content.lower():
            await message.channel.send("https://i.imgflip.com/86p8rc.gif")

        try:
            await message.add_reaction('🤓')
        except discord.DiscordException:
            pass

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(Events(bot))
