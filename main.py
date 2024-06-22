import discord
from discord.ext import commands
from discord import ui
from testpy import testresin
import tokendata

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents,
                   activity=discord.Game("$resin"))

@bot.event  # スラコマを登録
async def on_ready():
    print("ready!")
    await bot.change_presence(activity=discord.Game("Test Mode"))
    await bot.tree.sync()

class tokenModal(ui.Modal, title="Form"):  # モーダルを定義
    ltuid = ui.TextInput(label="ltuid")
    ltoken = ui.TextInput(label="ltoken")
    uid = ui.TextInput(label="uid", placeholder="800000000")

    async def on_submit(self, interaction: discord.Interaction):
        tokenDict = {
            "ltuid": self.ltuid.value,
            "ltoken": self.ltoken.value,
            "uid": self.uid.value
        }
        tokendata.save_token(tokenDict)
        await interaction.response.send_message("Register OK.", ephemeral=True)

@bot.tree.command(name="resin", description="Get Resin Data")
async def resin(interaction: discord.Interaction, text: int):
    tokendata.open_token()
    await interaction.response.send_message(text, ephemeral=True)

bot.run("MTI1NDA0MDU0Mzk3NDAwMjgxOQ.GWbq1i.gPhecI-QSrWuY3oNOadJaomjZlsOzXUHzvSpn4")
