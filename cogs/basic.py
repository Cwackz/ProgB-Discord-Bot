import discord
from discord import app_commands
from discord.ext import commands
from utils.database_utils import log_command  

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Responds with Pong!")
    async def ping(self, interaction: discord.Interaction):
        log_command("ping", interaction.user.id, interaction.channel.id)
        await interaction.response.send_message("Pong!")

    @app_commands.command(name="echo", description="Repeats the message")
    async def echo(self, interaction: discord.Interaction, message: str):
        log_command("echo", interaction.user.id, interaction.channel.id)
        await interaction.response.send_message(message)

    @app_commands.command(name="embed", description="Sends an embed")
    async def embed(self, interaction: discord.Interaction, title: str, description: str):
        log_command("embed", interaction.user.id, interaction.channel.id)
        embed = discord.Embed(title=title, description=description)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="Displays a list of commands")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Commands", color=discord.Colour.blue())
        commands = await self.bot.tree.fetch_commands()
        for command in commands:
            embed.add_field(name=command.name, value=command.description, inline=True)
    
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Basic(bot))
