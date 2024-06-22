import genshin
import asyncio
async def main():
    cookies = {"ltuid": 174808526, "ltoken": "ggetQDnMHo4Mt25qoeJi5pkdtWRkm4nHm8F3IZNx"}
    client = genshin.Client(cookies)

    data = await client.get_genshin_notes(845733927, lang="ja-jp")
    print(f"Your Current Resin: {data.current_resin}/{data.max_resin}")
    print(f"Remaining Resin Recovery Time: {data.remaining_resin_recovery_time}")

if __name__ == "__main__":
    asyncio.run(main())
