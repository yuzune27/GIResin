import discord
from discord.ext import commands
from discord import ui
import hoyouser
import tokendata
import json
from datetime import datetime, timedelta
from typing import Literal
import asyncio
import json

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

def selectID():
    IDList = []


@bot.event  # スラコマを登録
async def on_ready():
    print("ready!")
    await bot.change_presence(activity=discord.Game("/resin"))
    await bot.tree.sync()

class ValueManage():
    delUID = ""
    game = ""

class SelectGame(ui.View):
    def __init__(self):
        super().__init__()

    @ui.select(
        placeholder="ゲームを選択",
        options=[
            discord.SelectOption(label="原神", value="gi"),
            discord.SelectOption(label="崩壊：スターレイル", value="hsr")
        ]
    )
    async def selectMenu(self, interaction: discord.Interaction, select: ui.Select):
        ValueManage.game = select.values[0]
        await interaction.response.send_modal(tokenModal())
        embed = discord.Embed(title="フォーム入力", description="フォームでトークンを登録してください。", color=0x00ff00)
        await interaction.edit_original_response(embed=embed, view=None)

class tokenModal(ui.Modal, title="トークン入力フォーム"):  # モーダルを定義
    uid = ui.TextInput(label="UID", placeholder="800000000", min_length=9, max_length=10)
    ltuid = ui.TextInput(label="ltuid", min_length=9, max_length=9)
    ltoken = ui.TextInput(label="ltoken", min_length=40, max_length=40, style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        data = await hoyouser.user(self.ltuid.value, self.ltoken.value)
        if data == "Invalid Cookies":  # 整合性チェック1
            embed = discord.Embed(title="エラー", description="トークンが正しくありません。", timestamp=datetime.now(), color=0xff0000)
            embed.set_footer(text=data)
            await interaction.followup.send(embed=embed)
            return

        if data[0].uid == int(self.uid.value) or data[1].uid == int(self.uid.value):  # 整合性チェック2
            try:
                jsonData = tokendata.open_token()
            except json.decoder.JSONDecodeError:
                jsonData = {}
            else:
                if self.uid.value in jsonData:
                    embed = discord.Embed(title="エラー", description="このUIDは既に登録されています。", timestamp=datetime.now(), color=0xff0000)
                    await interaction.followup.send(embed=embed)
                    return
            newToken = {
                        "ltuid": int(self.ltuid.value),
                        "ltoken": self.ltoken.value,
                        "dcId": interaction.user.id
                        }
            jsonData[ValueManage.game][self.uid.value] = newToken
            tokendata.save_token(jsonData)
            embed = discord.Embed(title="登録完了", description=f"UIDを登録しました。\n`UID: {self.uid.value}`", timestamp=datetime.now(), color=0x00ff00)

            stat, name, icon = hoyouser.whichloginEnka(ValueManage.game, int(self.uid.value))
            if stat == 200:
                embed.set_author(name=name, icon_url=icon)
            else:
                pass
            await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(title="エラー", description="トークンが正しくありません。", timestamp=datetime.now(), color=0xff0000)
            embed.set_footer(text="Can't view other's profile.")
            await interaction.followup.send(embed=embed)

@bot.tree.command(name="addtoken", description="フォームでUIDを追加します。")
async def addtoken(interaction: discord.Interaction):
    embed = discord.Embed(title="トークン登録", description="ゲームを選択してください。", color=0x00ff00)
    await interaction.response.send_message(embed=embed, ephemeral=True, view=SelectGame())

class DelTokenButton(ui.View):
    def __init__(self):
        super().__init__()

    @ui.button(label="はい", style=discord.ButtonStyle.green)
    async def ok(self, interaction: discord.Interaction, button: ui.Button):
        jsonData = tokendata.open_token()
        del jsonData[ValueManage.game][ValueManage.delUID]
        tokendata.save_token(jsonData)
        embed = discord.Embed(title="削除完了", description=f"このUIDの登録を削除しました。\n`UID: {ValueManage.delUID}`", timestamp=datetime.now(), color=0x00ff00)
        await interaction.response.edit_message(embed=embed, view=None)
    
    @ui.button(label="いいえ", style=discord.ButtonStyle.gray)
    async def no(self, interaction: discord.Interaction, button: ui.Button):
        embed = discord.Embed(title="キャンセル", description="UIDの削除をキャンセルしました。", timestamp=datetime.now(), color=0x7d7d7d)
        await interaction.response.edit_message(embed=embed, view=None)

@bot.tree.command(name="deltoken", description="指定したUIDを削除します。")
@discord.app_commands.describe(game='原神="gi", 崩壊：スターレイル="hsr"', uid='登録したユーザIDを指定（9桁または10桁）')
async def deltoken(interaction: discord.Interaction, game: Literal["gi", "hsr"], uid: int):
    await interaction.response.defer(ephemeral=True, thinking=True)
    uid = str(uid)
    ValueManage.delUID = uid
    ValueManage.game = game
    jsonData = tokendata.open_token()
    idFound = False
    for jsonUID in jsonData[game]:
        if uid == jsonUID:
            if interaction.user.id == jsonData[game][uid]["dcId"]:
                embed = discord.Embed(title="削除確認", description=f"このUIDを削除しますか？\n`UID: {uid}`", timestamp=datetime.now(), color=0x00ff00)
                stat, name, icon = hoyouser.whichloginEnka(game, uid)
                if stat == 200:
                    embed.set_author(name=name, icon_url=icon)
                else:
                    pass
                await interaction.followup.send(embed=embed, ephemeral=True, view=DelTokenButton())
            else:
                embed = discord.Embed(title="エラー", description="このUIDの削除は、登録したDiscordアカウントのみ可能です。", timestamp=datetime.now(), color=0xff0000)
                await interaction.followup.send(embed=embed, ephemeral=True)
            idFound = True
            break
        else:
            pass

    if not idFound:
        embed = discord.Embed(title="エラー", description="このUIDは登録されていません。", timestamp=datetime.now(), color=0xff0000)
        await interaction.followup.send(embed=embed, ephemeral=True)

@bot.tree.command(name="daily", description="ログインボーナスを取得します。")
@discord.app_commands.describe(game='原神="gi", 崩壊：スターレイル="hsr"', uid='登録したユーザIDを指定（9桁または10桁）')
async def daily(interaction: discord.Interaction, game: Literal["gi", "hsr"], uid: int):
    await interaction.response.defer(ephemeral=True, thinking=True)
    uid = str(uid)
    jsonData = tokendata.open_token()
    idFound = False
    for jsonUID in jsonData[game]:
        if uid == jsonUID:
            name, amount, icon = await hoyouser.daily(game, jsonData[game][uid]["ltuid"], jsonData[game][uid]["ltoken"])
            if "AlreadyClaimed" in str(name):
                embed = discord.Embed(title="ログインボーナス", description="すでにログインボーナスは受取済みです。", timestamp=datetime.now(), color=0x00b0f4)
            else:
                embed = discord.Embed(title="ログインボーナス", description=f"次の報酬を獲得しました！\n```{name} x{amount}```", timestamp=datetime.now(), color=0x00b0f4)
                embed.set_thumbnail(url=icon)

            stat, name, icon = hoyouser.whichloginEnka(game, uid)
            if stat == 200:
                embed.set_author(name=name, icon_url=icon)
            else:
                pass
            embed.set_footer(text=f"UID: {uid}")
            idFound = True
            break

    if not idFound:
        embed = discord.Embed(title="エラー", description="このUIDは登録されていません。", timestamp=datetime.now(), color=0xff0000)
    await interaction.followup.send(embed=embed)


@bot.tree.command(name="resin", description="天然樹脂の情報を取得します。")
@discord.app_commands.describe(uid='登録したユーザIDを指定（9桁または10桁）')
async def resin(interaction: discord.Interaction, uid: int):
    await interaction.response.defer(ephemeral=True, thinking=True)
    uid = str(uid)
    jsonData = tokendata.open_token()
    idFound = False
    for jsonUID in jsonData["gi"]:
        if uid == jsonUID:
            cResin, mResin, reResin = await hoyouser.resin(jsonData["gi"][uid]["ltuid"], jsonData["gi"][uid]["ltoken"], uid)
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
            stat, name, icon = hoyouser.loginEnka(uid)
            if stat == 200:
                embed.set_author(name=name, icon_url=icon)
            else:
                pass
            embed.set_footer(text=f"UID: {uid}")
            idFound = True
            break
        else:
            pass
    if not idFound:
        embed = discord.Embed(title="エラー", description="このUIDは登録されていません。", color=0xff0000)
    await interaction.followup.send(embed=embed)

class BotStopButton(ui.View):
    def __init__(self):
        super().__init__()

    @ui.button(label="はい", style=discord.ButtonStyle.green)
    async def ok(self, interaction: discord.Interaction, button: ui.Button):
        embed = discord.Embed(title="停止", description="Botを停止しました。", timestamp=datetime.now(), color=0x00ff00)
        await interaction.response.edit_message(embed=embed, view=None)
        await bot.close()
    
    @ui.button(label="いいえ", style=discord.ButtonStyle.gray)
    async def no(self, interaction: discord.Interaction, button: ui.Button):
        embed = discord.Embed(title="キャンセル", description="起動終了をキャンセルしました。", timestamp=datetime.now(), color=0x7d7d7d)
        await interaction.response.edit_message(embed=embed, view=None)

@bot.tree.command(name="stop", description="Botを停止します（ボット所有者のみ）。")
@commands.is_owner() 
async def stop(interaction: discord.Interaction):
    if interaction.user.id == 577051552582205460:
        embed = discord.Embed(title="Bot停止", description="Botを停止します。", color=0x00ff00)
        await interaction.response.send_message(embed=embed, view=BotStopButton(), ephemeral=True)
    else:
        embed = discord.Embed(title="エラー", description="権限がありません。", timestamp=datetime.now(), color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

bot.run(config["BotToken"])
