# animal-bot/bot/config.py
# author: Mofumii
# version 1.0


import os
from dotenv import load_dotenv

load_dotenv()
BOT_API_TOKEN = os.getenv("BOT_API_TOKEN")