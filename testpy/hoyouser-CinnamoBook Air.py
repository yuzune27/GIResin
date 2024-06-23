import genshin
import asyncio


async def user(ltuid, ltoken):
    cookies = {"ltuid": ltuid, "ltoken": ltoken}
    client = genshin.Client(cookies)

    data = await client.get_record_cards(ltuid)
    print(data)
    with open ("user.txt", "w", encoding="utf-8") as f:
        f.write(str(data))


async def resin(ltuid, ltoken, uid):
    cookies = {"ltuid": ltuid, "ltoken": ltoken}
    client = genshin.Client(cookies)

    data = await client.get_genshin_notes(uid, lang="ja-jp")
    txt1 = f"Your Current Resin: {data.current_resin}/{data.max_resin}\n"
    txt2 = f"Remaining Resin Recovery Time: {data.remaining_resin_recovery_time}"

    txt = txt1 + txt2
    return txt

if __name__ == "__main__":
    asyncio.run(user(174808526, "ggetQDnMHo4Mt25qoeJi5pkdtWRkm4nHm8F3IZNx"))
