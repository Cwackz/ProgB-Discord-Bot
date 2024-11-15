import discord
from discord.ext import commands
from discord import app_commands
from utils.database_utils import create_user, login_user, logout_user

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="register", description="Register a new user with a username and password")
    async def register(self, interaction: discord.Interaction, username: str, password: str):
        if create_user(username, password):
            await interaction.response.send_message("Registration successful!", ephemeral=True)
        else:
            await interaction.response.send_message("Username already exists or an error occurred.", ephemeral=True)

    @app_commands.command(name="login", description="Login with your username and password")
    async def login(self, interaction: discord.Interaction, username: str, password: str):
        if login_user(username, password):
            await interaction.response.send_message("Login successful!", ephemeral=True)
        else:
            await interaction.response.send_message("Invalid username or password.", ephemeral=True)

    @app_commands.command(name="logout", description="Logout from the system")
    async def logout(self, interaction: discord.Interaction):
        if logout_user(interaction.user.id):
            await interaction.response.send_message("Logout successful.", ephemeral=True)
        else:
            await interaction.response.send_message("You are not logged in.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))
