import genshin
import asyncio

async def main():
    client = genshin.Client()
    cookies = await client.login_with_password("yzkittybot@gmail.com", "jW7rgP32")
    data = await genshin.complete_cookies(cookies)
    print(data)

asyncio.run(main())