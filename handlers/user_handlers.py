from loader import app
from pyrogram import filters

@app.on_message(filters.private)
async def hello(client, message):
    await message.reply("Hello from Pyrogram!")