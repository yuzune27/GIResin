import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print("ready!")
    await bot.change_presence(activity=discord.Game("Test Mode"))
    await bot.tree.sync()


@bot.tree.command(name="test", description="This is Test")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("test OK!")

bot.run("MTI1NDA0MDU0Mzk3NDAwMjgxOQ.GWbq1i.gPhecI-QSrWuY3oNOadJaomjZlsOzXUHzvSpn4")
