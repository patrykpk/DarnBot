import os

from PerformCommands import *

from discord import File, Embed
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")

@bot.command(name="build")
async def ChampionBuild(ctx, Champion):
	Argument = "build"
	DiscordInput(Argument, Champion)
	await ctx.send("Retrieved this Build for {}:".format(Champion))
	await ctx.send(file=File("./BuildItems/FullBuild.png"))
	DeleteImages()

@bot.command(name="clear")
async def ClearMessages(ctx, AmountMessages = 4):
	await ctx.channel.purge(limit=AmountMessages)

@bot.command(name="made")
async def MadeBy(ctx):
	await ctx.send(embed=Embed(description="DarnBot was made by Patryk Krzyzaniak"))

bot.run(token)


