from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot:Bot):
    commands = [
        BotCommand(
            command="start",
            description="Начать работу с ботом"
        ),
        BotCommand(
            command="help",
            description="Помощь"
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())