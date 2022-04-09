from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db.storage import DatabaseManager

from data.config import BOT_TOKEN, DB_URL


bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DatabaseManager(DB_URL)