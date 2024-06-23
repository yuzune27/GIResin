import genshin
import asyncio
from datetime import datetime, timedelta


async def user(ltuid, ltoken):
    cookies = {"ltuid": ltuid, "ltoken": ltoken}
    client = genshin.Client(cookies, lang="ja-jp")

    try:
        data = await client.get_record_cards(ltuid)
    except genshin.InvalidCookies as e:
        return "Invalid Cookies"
    return data

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
    asyncio.run(resin(174808526, "ggetQDnMHo4Mt25qoeJi5pkdtWRkm4nHm8F3IZNx", 845733927))