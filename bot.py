import discord
from discord.ext import commands
import os
from utils.token_utils import get_token

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Slash commands synced for guild.")
    print(f"Logged in as {bot.user}")

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def setup_hook():
    await load_cogs()

bot.run(get_token())
