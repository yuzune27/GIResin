import genshin
import asyncio
from datetime import datetime, timedelta
import requests
import json
import re


async def user(ltuid, ltoken):
    cookies = {"ltuid_v2": ltuid, "ltoken_v2": ltoken}
    client = genshin.Client(cookies, lang="ja-jp")

    try:
        data = await client.get_record_cards(ltuid)
    except genshin.InvalidCookies as e:
        return "Invalid Cookies"
    return data

def loginEnka(uid):
    url = f"https://enka.network/api/uid/{uid}?info"
    res = requests.get(url)
    if res.status_code == 200:
        jsonData = res.json()
        name = jsonData["playerInfo"]["nickname"]
        try:
            iconID = jsonData["playerInfo"]["profilePicture"]["id"]
        except KeyError:
            iconID = jsonData["playerInfo"]["profilePicture"]["avatarId"]
            chara = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/characters.json"
            res2 = requests.get(chara).json()
            icon = res2[str(iconID)]["SideIconName"]
            icon = str(icon).replace("UI_AvatarIcon_Side", "UI_AvatarIcon")
        else:
            pfps = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/pfps.json"
            res2 = requests.get(pfps).json()
            icon = res2[str(iconID)]["iconPath"]


        iconUrl = f"https://enka.network/ui/{icon}.png"

        return res.status_code, name, iconUrl
    else:
        return res.status_code, None, None
    
def loginHSREnka(uid):
    url = f"https://enka.network/api/hsr/uid/{uid}"
    res = requests.get(url)
    if res.status_code == 200:
        jsonData = res.json()
        name = jsonData["detailInfo"]["nickname"]
        iconID = jsonData["detailInfo"]["headIcon"]

        avatars = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/hsr/honker_avatars.json"
        res2 = requests.get(avatars).json()
        icon = res2[str(iconID)]["Icon"]

        iconUrl = f"https://enka.network/ui/hsr/{icon}"

        return res.status_code, name, iconUrl
    else:
        return res.status_code, None, None
    
def whichloginEnka(game, uid):
    if game == "gi":
        stat, name, icon = loginEnka(uid)
    elif game == "hsr":
        stat, name, icon = loginHSREnka(uid)
    return stat, name, icon

async def daily(game, ltuid, ltmid, ltoken):
    if game == "gi":
        game = genshin.Game.GENSHIN
    elif game == "hsr":
        game = genshin.Game.STARRAIL
    try:
        cookies = {"ltuid_v2": ltuid, "ltmid_v2": ltmid, "ltoken_v2": ltoken}
        client = genshin.Client(cookies, lang="ja-jp")

        data = await client.claim_daily_reward(game=game)
    except Exception as e:
        return e.__class__, None, None
    else:
        return data.name, data.amount, data.icon


async def genshinNotes(ltuid, ltoken, uid):
    cookies = {"ltuid_v2": ltuid, "ltoken_v2": ltoken}
    client = genshin.Client(cookies, lang="ja-jp")

    data = await client.get_genshin_notes(uid)

    return data


async def hsrNotes(ltuid, ltoken, uid):
    cookies = {"ltuid_v2": ltuid, "ltoken_v2": ltoken}
    client = genshin.Client(cookies, lang="ja-jp")

    data = await client.get_starrail_notes(uid)

    return data


def event():

    def toJst(dt):
        dt = datetime.strptime(dt, "%Y/%m/%d %H:%M:%S")
        dtJST = dt + timedelta(hours=1)
        return dtJST


    url = "https://api.ambr.top/assets/data/event.json"
    resp = requests.get(url).json()

    for r in resp:
        name = resp[r]["name"]["JP"]
        descJP = resp[r]["description"]["JP"]
        pattern = re.compile(r'<t class="t_lc">(.*?)</t>')

        getDt = re.findall(pattern, descJP)
        try:
            startDt = toJst(getDt[0])
            endDt = toJst(getDt[1])
        except IndexError:
            startDt = "常設"
            endDt = None

        if name == "アップデート詳細":
            continue
        if "紀行" in name:
            startDt = "アップデート後"
            endDt = toJst(getDt[0])

        print(name)
        print(startDt)
        print(endDt)
        print()

if __name__ == "__main__":
    print("---Test Space---")
    event()
    print("---End---")