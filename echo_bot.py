import os
import discord
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
XM_BOT_ID = int(os.getenv('XM_BOT_ID'))

# set intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# initialize
client = discord.Client(intents=intents)

# when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    print(client.user.id)

# when the bot gets a message
@client.event
async def on_message(message):
    # ignore bot's own messages or xm bot's messages
    if message.author == client.user or \
       message.author.id == XM_BOT_ID:
        return
    
    # for file attachments
    if message.attachments:
        for attachment in message.attachments:
            try:
                await attachment.save(attachment.filename)
                file = discord.File(attachment.filename)
                await message.channel.send(message.content, file=file)
                os.remove(attachment.filename)
            except discord.errors.HTTPException:
                await print("Failed to send attachment")
    else: 
        # echo others' messages
        await message.channel.send(message.content)

# start the bot
client.run(BOT_TOKEN)