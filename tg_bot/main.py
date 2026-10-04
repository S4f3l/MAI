from aiogram import Bot, Dispatcher, types
import asyncio
from core.handlers.basic import get_start, help_command
from core.settings import settings
from aiogram.filters import Command
from core.utuls.commands import set_commands
from aiogram.filters import Text
from core.keyboard.reply import reply_keyboard2

bot = Bot(token ="6645785798:AAE8WN8kWFSUxMMjv3OM6SKxVwkuKx_LxTw")
dp = Dispatcher()
# dp.message.register(help_command, Command(commands=["help"]))
# dp.message.register(get_start, Command(commands=["start"]))

# @dp.message(Text("Каталог"))
# async def buttons(message:types.Message):
#     keyboard = types.ReplyKeyboardMarkup(keyboard=reply_keyboard2, resize_keyboard=True)
#     await message.answer("21312")
@dp.message(Command("start"))
async def lol(message: types.Message):
    await message.answer("Рад тебя видеть)")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())