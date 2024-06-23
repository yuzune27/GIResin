import discord
from discord.ext import commands
from discord import ui
import hoyouser
import tokendata
import json
from datetime import datetime, timedelta
from typing import Literal

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
        data = await hoyouser.user(self.ltuid.value, self.ltoken.value)
        if data == "Invalid Cookies":
            embed = discord.Embed(title="エラー", description="トークンが正しくありません。", color=0xff0000)
            embed.set_footer(text=data)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if data[0].uid == int(self.uid.value):
            try:
                jsonData = tokendata.open_token()
            except json.decoder.JSONDecodeError:
                jsonData = {}
            else:
                if self.uid.value in jsonData:
                    embed = discord.Embed(title="エラー", description="このUIDは既に登録されています。", color=0xff0000)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
            newToken = {
                        "ltuid": int(self.ltuid.value),
                        "ltoken": self.ltoken.value,
                        "dcId": interaction.user.id
                        }
            jsonData[self.uid.value] = newToken
            tokendata.save_token(jsonData)
            embed = discord.Embed(title="登録完了", description=f"UIDを登録しました。\n`UID: {self.uid.value}`", color=0x00ff00)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="エラー", description="トークンが正しくありません。", color=0xff0000)
            embed.set_footer(text="Can't view other's profile.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="addtoken", description="フォームでトークンを追加します。")
async def addtoken(interaction: discord.Interaction):
    modal = tokenModal()
    await interaction.response.send_modal(modal)

@bot.tree.command(name="deltoken", description="指定したトークンを削除します。")
@discord.app_commands.describe(uid='登録したユーザIDを指定（9桁または10桁）')
async def deltoken(interaction: discord.Interaction, uid: int):
    uid = str(uid)
    jsonData = tokendata.open_token()
    if uid in jsonData:
        del jsonData[uid]
        tokendata.save_token(jsonData)
        embed = discord.Embed(title="削除完了", description=f"このUIDの登録を削除しました。\n`UID: {uid}`", color=0x00ff00)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="エラー", description="このUIDは登録されていません。", color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="daily", description="ログインボーナスを取得します。")
@discord.app_commands.describe(game='原神="gi", 崩壊：スターレイル="hsr"', uid='登録したユーザIDを指定（9桁または10桁）')
async def daily(interaction: discord.Interaction, game: Literal["gi", "hsr"], uid: int):
    uid = str(uid)
    jsonData = tokendata.open_token()
    if game == "gi" or game == "hsr":
        if uid in jsonData:
            name, amount, icon = await hoyouser.daily(game, jsonData[uid]["ltuid"], jsonData[uid]["ltoken"])
            if "AlreadyClaimed" in str(name):
                embed = discord.Embed(title="ログインボーナス", description="すでにログインボーナスは受取済みです。", color=0x00b0f4)
            elif "genshinException" in str(name):
                embed = discord.Embed(title="エラー", description="アカウントはこのゲームに存在しません。", color=0xff0000)
            else:
                embed = discord.Embed(title="ログインボーナス", description=f"次の報酬を獲得しました！\n```{name} x{amount}```", color=0x00b0f4)
                embed.set_thumbnail(url=icon)
        else:
            embed = discord.Embed(title="エラー", description="このUIDは登録されていません。", color=0xff0000)
    else:
        embed = discord.Embed(title="エラー", description="ゲーム名が正しくありません。", color=0xff0000)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="resin", description="天然樹脂の情報を取得します。")
@discord.app_commands.describe(uid='登録したユーザIDを指定（9桁または10桁）')
async def resin(interaction: discord.Interaction, uid: int):
    uid = str(uid)
    jsonData = tokendata.open_token()
    if uid in jsonData:
        cResin, mResin, reResin = await hoyouser.resin(jsonData[uid]["ltuid"], jsonData[uid]["ltoken"], uid)
        if cResin == mResin:
            bemResin = "全回復しました。"
        else:
            dtNow = datetime.now()
            bemDt = dtNow + timedelta(days=reResin.days, seconds=reResin.seconds)
            bemResin = f"{bemDt:%m/%d %H:%M:%S}に全回復"
        embed = discord.Embed(title="天然樹脂情報",
                            colour=0x00b0f4,
                            timestamp=datetime.now())

        embed.add_field(name="現在の天然樹脂",
                        value=f"```{cResin}/{mResin}```",
                        inline=False)
        embed.add_field(name="回復残り時間",
                        value=f"```あと{reResin}\n({bemResin})```",
                        inline=False)
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/gensin-impact/images/3/35/Item_Fragile_Resin.png/")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="エラー", description="このUIDは登録されていません。", color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class ConfirmButton(ui.View):
    def __init__(self):
        super().__init__()

    @ui.button(label="はい", style=discord.ButtonStyle.green)
    async def ok(self, interaction: discord.Interaction, button: ui.Button):
        embed = discord.Embed(title="停止", description="Botを停止しました。", color=0x00ff00)
        await interaction.response.edit_message(embed=embed, view=None)
        await bot.close()
    
    @ui.button(label="いいえ", style=discord.ButtonStyle.gray)
    async def no(self, interaction: discord.Interaction, button: ui.Button):
        embed = discord.Embed(title="キャンセル", description="起動終了をキャンセルしました。", color=0x7d7d7d)
        await interaction.response.edit_message(embed=embed, view=None)

@bot.tree.command(name="stop", description="Botを停止します（ボット所有者のみ）。")
@commands.is_owner() 
async def stop(interaction: discord.Interaction):
    if interaction.user.id == 577051552582205460:
        embed = discord.Embed(title="Bot停止", description="Botを停止します。", color=0x00ff00)
        await interaction.response.send_message(embed=embed, view=ConfirmButton(), ephemeral=True)
    else:
        embed = discord.Embed(title="エラー", description="権限がありません。", color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run("MTI1NDA0MDU0Mzk3NDAwMjgxOQ.GWbq1i.gPhecI-QSrWuY3oNOadJaomjZlsOzXUHzvSpn4")
