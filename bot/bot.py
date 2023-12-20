import discord
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[799848795050606604])
async def hello(ctx):
    await ctx.respond("Hello!")

bot.run(os.getenv('bot_token'))