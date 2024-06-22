import discord


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('MTI1NDA0MDU0Mzk3NDAwMjgxOQ.GWbq1i.gPhecI-QSrWuY3oNOadJaomjZlsOzXUHzvSpn4')
