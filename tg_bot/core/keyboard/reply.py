from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType


reply_keyboard1 = ReplyKeyboardMarkup(keyboard = [
    [
        KeyboardButton(
            text = "Каталог"
        ),
        KeyboardButton(
            text = "Курс"
        ),
    ],
    [
        KeyboardButton(
            text = "Помощь"
        )
    ]
], resize_keyboard = True, one_time_keyboard = True, input_field_placeholder="Выбери кнопку")

reply_keyboard2 = ReplyKeyboardMarkup(keyboard = [
    [
        KeyboardButton(
            text = "23"
        )
    ]
])