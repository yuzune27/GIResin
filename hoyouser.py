import genshin
import asyncio
from datetime import datetime, timedelta


async def user(ltuid, ltoken):
    cookies = {"ltuid": ltuid, "ltoken": ltoken}
    client = genshin.Client(cookies)

    data = await client.get_record_cards(ltuid)

async def daily(ltuid, ltoken):
    try:
        cookies = {"ltuid": ltuid, "ltoken": ltoken}
        client = genshin.Client(cookies)

        data = await client.claim_daily_reward(lang="ja-jp", game="genshin")
    except genshin.AlreadyClaimed:
        print("本日のデイリー報酬は既に受取済みです。")
    else:
        print(f"次の報酬を獲得しました！\n {data.reward.name} x{data.reward.amount}")


async def resin(ltuid, ltoken, uid):
    cookies = {"ltuid": ltuid, "ltoken": ltoken}
    client = genshin.Client(cookies)

    data = await client.get_genshin_notes(uid, lang="ja-jp")

    return data.current_resin, data.max_resin, data.remaining_resin_recovery_time

if __name__ == "__main__":
    x, y, z = asyncio.run(resin(174808526, "ggetQDnMHo4Mt25qoeJi5pkdtWRkm4nHm8F3IZNx", "845733927"))
    dtNow = datetime.now()
    dtNext = dtNow + timedelta(days=z.days, seconds=z.seconds)
    m, s = divmod(z.seconds, 60)
    h, m = divmod(m, 60)
    print(f"{z.days}日 {h}時間{m}分{s}秒")
    print(f"{dtNext:%m/%d %H:%M:%S}")