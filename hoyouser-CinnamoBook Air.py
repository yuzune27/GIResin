import genshin
import asyncio


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
    asyncio.run(user(174808526, "ggetQDnMHo4Mt25qoeJi5pkdtWRkm4nHm8F3IZNx"))
