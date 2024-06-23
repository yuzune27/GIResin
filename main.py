import discord
from discord.ext import commands
from discord import ui
from testpy import testresin
import tokendata
import json

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event  # スラコマを登録
async def on_ready():
    print("ready!")
    await bot.change_presence(activity=discord.Game("/resin"))
    await bot.tree.sync()

class tokenModal(ui.Modal, title="Add Token Form"):  # モーダルを定義
    uid = ui.TextInput(label="UID", placeholder="800000000", min_length=9, max_length=10)
    ltuid = ui.TextInput(label="ltuid", min_length=9, max_length=9)
    ltoken = ui.TextInput(label="ltoken", min_length=40, max_length=40)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            jsonData = tokendata.open_token()
        except json.decoder.JSONDecodeError:
            jsonData = {}
        else:
            if self.uid.value in jsonData:
                await interaction.response.send_message("This UID is already registered.", ephemeral=True)
                return
        newToken = {
                    "ltuid": int(self.ltuid.value),
                    "ltoken": self.ltoken.value,
                    }
        jsonData[self.uid.value] = newToken
        tokendata.save_token(jsonData)
        await interaction.response.send_message(f"Register OK.\nUID:{self.uid.value}", ephemeral=True)

@bot.tree.command(name="addtoken", description="Add Your Token with Modal")
async def addtoken(interaction: discord.Interaction):
    modal = tokenModal()
    await interaction.response.send_modal(modal)

@bot.tree.command(name="deltoken", description="Delete Your Token")
async def deltoken(interaction: discord.Interaction, text: int):
    text = str(text)
    jsonData = tokendata.open_token()
    if text in jsonData:
        del jsonData[text]
        tokendata.save_token(jsonData)
        await interaction.response.send_message(f"Delete OK.\nUID: {text}", ephemeral=True)
    else:
        await interaction.response.send_message("This UID is not registered.", ephemeral=True)

@bot.tree.command(name="resin", description="Get Resin Data")
async def resin(interaction: discord.Interaction, text: int):
    text = str(text)
    jsonData = tokendata.open_token()
    if text in jsonData:
        resp = await testresin.main(jsonData[text]["ltuid"], jsonData[text]["ltoken"], text)
        await interaction.response.send_message(resp, ephemeral=True)
    else:
        await interaction.response.send_message("This UID is not registered.", ephemeral=True)

bot.run("MTI1NDA0MDU0Mzk3NDAwMjgxOQ.GWbq1i.gPhecI-QSrWuY3oNOadJaomjZlsOzXUHzvSpn4")
