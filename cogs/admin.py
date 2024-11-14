import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal, Optional
from utils.database_utils import get_command_logs, log_command 

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="purge", description="Purges messages")
    async def purge(self, interaction: discord.Interaction, amount: int):
        log_command("purge", interaction.user.id, interaction.channel.id)
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"Purged {amount} messages!")

    @app_commands.command(name="stop", description="Stops the bot")
    async def stop(self, interaction: discord.Interaction):
        log_command("stop", interaction.user.id, interaction.channel.id)
        await interaction.response.send_message("Goodbye!")
        await self.bot.close()

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None):
        if not guilds:
            if spec == "~":
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                self.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                self.bot.tree.clear_commands(guild=ctx.guild)
                synced = await self.bot.tree.sync(guild=ctx.guild)
            else:
                synced = await self.bot.tree.sync()

            await ctx.send(f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}")
            return

        ret = 0
        for guild in guilds:
            try:
                await self.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
        
    @app_commands.command(name="logs", description="Displays recent command logs")
    @commands.is_owner()  
    async def logs(self, interaction: discord.Interaction, limit: int = 10):
        logs = get_command_logs(limit)
        if not logs:
            await interaction.response.send_message("No command logs found.")
            return

        embed = discord.Embed(title=f"Command Logs (last {limit} commands)", color=discord.Colour.blue())
        for log in logs:
            command_name = log[1]
            user_mention = f"<@{log[2]}>"
            channel_mention = f"<#{log[3]}>"
            timestamp = log[4]

            embed.add_field(
                name=f"Command: {command_name}",
                value=f"**User:** {user_mention}\n**Channel:** {channel_mention}\n**Time:** {timestamp}",
                inline=False
            )

        

async def setup(bot):
    await bot.add_cog(Admin(bot))
