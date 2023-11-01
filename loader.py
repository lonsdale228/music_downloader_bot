import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN=os.getenv('BOT_TOKEN')
app = Client("music_bot")