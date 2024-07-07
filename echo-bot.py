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
bot_running = False

# when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

# when the bot gets a message
@client.event
async def on_message(message):
    global bot_running
    if message.content == "echo start":
        if bot_running:
            await message.channel.send("Echo is already running")
        else:
            bot_running = True
            await message.channel.send("Echo is back")
        return
    
    if message.content == "echo stop":
        if bot_running:
            bot_running = False
            await message.channel.send("Echo out")
        return

    if not bot_running:
        return

    # ignore the bot's own messages or xm bot's messages
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
                print("Failed to send attachment")
    else: 
        # echo others' messages
        try:
            await message.channel.send(message.content)
        except discord.errors.HTTPException:
            print("Failed to send the message")

# when a user reacts to a message
@client.event
async def on_raw_reaction_add(payload):
    if not bot_running:
        return
    
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
        
    # ignore the bot's own reaction
    if payload.member == client.user:
        return
    
    # send the same reaction
    await message.add_reaction(payload.emoji)

# start the bot
client.run(BOT_TOKEN)