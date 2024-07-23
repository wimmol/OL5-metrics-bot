from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN_DEV')
bot = Bot(token=TOKEN)
