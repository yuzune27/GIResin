import genshin
import asyncio

async def main():
    try:
        cookies = {"ltuid": 174808526, "ltoken": "ggetQDnMHo4Mt25qoeJi5pkdtWRkm4nHm8F3IZNx"}
        client = genshin.Client(cookies)

        data = await client.claim_daily_reward(lang="ja-jp", game="genshin")
    except genshin.AlreadyClaimed:
        print("本日のデイリー報酬は既に受取済みです。")
    else:
        print(f"次の報酬を獲得しました！\n {data.reward.name} x{data.reward.amount}")

asyncio.run(main())
