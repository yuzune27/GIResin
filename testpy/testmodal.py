import discord
from discord import app_commands
from discord.ext import commands
from discord import ui
import testresin

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="$", intents=intents)

class Modal(ui.Modal, title="自己紹介"):
    name = ui.TextInput(label="お名前")
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"ようこそ、{self.name.value}さん!")

@bot.event
async def on_ready():
    print("ready!")
    await bot.change_presence(activity=discord.Game("Test Mode"))
    await bot.tree.sync()


@bot.tree.command(name="test", description="This is Test")
async def test(interaction: discord.Interaction):
    modal = Modal()
    await interaction.response.send_modal(modal)

bot.run("MTI1NDA0MDU0Mzk3NDAwMjgxOQ.GWbq1i.gPhecI-QSrWuY3oNOadJaomjZlsOzXUHzvSpn4")
