import genshin
import asyncio
from datetime import datetime, timedelta
import requests


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

async def daily(game, ltuid, ltoken):
    if game == "gi":
        game = genshin.Game.GENSHIN
    elif game == "hsr":
        game = genshin.Game.STARRAIL
    try:
        cookies = {"ltuid_v2": ltuid, "ltoken_v2": ltoken}
        client = genshin.Client(cookies, lang="ja-jp")

        data = await client.claim_daily_reward(game=game)
    except Exception as e:
        return e.__class__, None, None
    else:
        return data.name, data.amount, data.icon


async def resin(ltuid, ltoken, uid):
    cookies = {"ltuid_v2": ltuid, "ltoken_v2": ltoken}
    client = genshin.Client(cookies, lang="ja-jp")

    data = await client.get_genshin_notes(uid)

    return data.current_resin, data.max_resin, data.remaining_resin_recovery_time

if __name__ == "__main__":
    data = asyncio.run(user(174808526, "ggetQDnMHo4Mt25qoeJi5pkdtWRkm4nHm8F3IZNx"))
    print(data[1])