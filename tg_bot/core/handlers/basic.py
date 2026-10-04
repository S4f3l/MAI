from aiogram import Bot
from aiogram.types import Message
from core.keyboard.reply import reply_keyboard1

async def get_start(message:Message, bot: Bot):
    await bot.send_message(message.from_user.id, f"{message.from_user.first_name},"
                                                 f"Приветсвуем в боте онлайн магазина KIXSTOCK",
                                                 reply_markup=reply_keyboard1)

async def help_command(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id,
                           "/help - помощь\n/start - начать работу с ботом",
                            reply_markup=reply_keyboard1)
