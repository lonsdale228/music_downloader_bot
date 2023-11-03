import asyncio

from loader import app
from pyrogram.types import Message
from pyrogram import filters

from utils.downloader import download_video



async def check_for_url(url):
    ...

@app.on_message(filters.private)
async def hello(client, message:Message):
    msg_to_edit=await message.reply("Download started!")
    out_path,audio_name=await download_video(message.text,message.from_user.id,msg_to_edit)
    # audio=open(out_path,'rb')
    await message.reply_audio(out_path,title=audio_name)
    # audio.close()