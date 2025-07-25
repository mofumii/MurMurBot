# animal-bot/bot/bot.py
# author: mofumii
# version 1.0


from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_API_TOKEN

bot = Bot(token=BOT_API_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()