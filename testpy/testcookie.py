import genshin
import asyncio

async def simpleCookies():
    client = genshin.Client()
    cookies = await client.login_with_password("yzkittybot@gmail.com", "jW7rgP32")
    return cookies.account_id_v2

async def fullCookies(cookies):
    data = await genshin.complete_cookies(cookies)
    print(data)

async def main():
    cookies = await simpleCookies()
    await fullCookies(cookies)

asyncio.run(main())