import genshin
import asyncio
from datetime import datetime, timedelta
import requests


async def user(ltuid, ltoken):
    cookies = {"ltuid": ltuid, "ltoken": ltoken}
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
        iconID = jsonData["playerInfo"]["profilePicture"]["id"]

        pfps = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/pfps.json"
        res2 = requests.get(pfps).json()
        icon = res2[str(iconID)]["iconPath"]

        iconUrl = f"https://enka.network/ui/{icon}.png"

        return res.status_code, name, iconUrl
    else:
        return res.status_code, None, None

async def daily(game, ltuid, ltoken):
    if game == "gi":
        game = genshin.Game.GENSHIN
    elif game == "hsr":
        game = genshin.Game.STARRAIL
    try:
        cookies = {"ltuid": ltuid, "ltoken": ltoken}
        client = genshin.Client(cookies, lang="ja-jp")

        data = await client.claim_daily_reward(game=game)
    except Exception as e:
        return e.__class__, None, None
    else:
        return data.name, data.amount, data.icon


async def resin(ltuid, ltoken, uid):
    cookies = {"ltuid": ltuid, "ltoken": ltoken}
    client = genshin.Client(cookies, lang="ja-jp")

    data = await client.get_genshin_notes(uid)

    return data.current_resin, data.max_resin, data.remaining_resin_recovery_time

if __name__ == "__main__":
    x, y, z = loginEnka(845733927)
    print(x)
    print(y)
    print(z)