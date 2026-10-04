import asyncio
import aiohttp
import datetime
import matplotlib.pyplot as plt
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
import locale
import io

API_TOKEN = '8151205874:AAFseY-2RRBj85p3vV1lmG1kH8M4DdDDZrw'

CBR_API = "https://www.cbr-xml-daily.ru/daily_json.js"
COIN_API = "https://api.coingecko.com/api/v3/simple/price"
COIN_MARKET_CHART_API = "https://api.coingecko.com/api/v3/coins/{id}/market_chart"

locale.setlocale(locale.LC_ALL, '')

FIAT_CURRENCIES = {
    "USD": {"ru": "Доллар США", "en": "US Dollar"},
    "EUR": {"ru": "Евро", "en": "Euro"},
    "GBP": {"ru": "Фунт стерлингов", "en": "Pound Sterling"},
    "JPY": {"ru": "Японская иена", "en": "Japanese Yen"},
    "CNY": {"ru": "Китайский юань", "en": "Chinese Yuan"},
    "CHF": {"ru": "Швейцарский франк", "en": "Swiss Franc"},
    "AUD": {"ru": "Австралийский доллар", "en": "Australian Dollar"},
    "CAD": {"ru": "Канадский доллар", "en": "Canadian Dollar"},
    "SEK": {"ru": "Шведская крона", "en": "Swedish Krona"},
    "NOK": {"ru": "Норвежская крона", "en": "Norwegian Krone"},
}

CRYPTO_CURRENCIES = {
    "bitcoin": {"ru": "Биткоин", "en": "Bitcoin"},
    "ethereum": {"ru": "Эфириум", "en": "Ethereum"},
    "litecoin": {"ru": "Лайткоин", "en": "Litecoin"},
    "dogecoin": {"ru": "Догикоин", "en": "Dogecoin"},
    "solana": {"ru": "Солана", "en": "Solana"},
    "toncoin": {"ru": "Тонкоин", "en": "Toncoin"},
    "avalanche-2": {"ru": "Аваланш", "en": "Avalanche"},
    "tron": {"ru": "Трон", "en": "Tron"},
    "polkadot": {"ru": "Полкадот", "en": "Polkadot"},
}

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- utils ---

async def fetch_json(url, params=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json(content_type=None)

async def get_fiat_rates():
    data = await fetch_json(CBR_API)
    rates = {}
    valutes = data.get("Valute", {})
    for code in FIAT_CURRENCIES.keys():
        v = valutes.get(code)
        if v:
            rates[code] = v["Value"]
    return rates

async def get_crypto_rates():
    ids = ",".join(CRYPTO_CURRENCIES.keys())
    params = {"ids": ids, "vs_currencies": "rub,usd"}
    data = await fetch_json(COIN_API, params)
    rates = {}
    for coin_id in CRYPTO_CURRENCIES.keys():
        coin_data = data.get(coin_id, {})
        rub = coin_data.get("rub")
        if rub is not None:
            rates[coin_id] = rub
    return rates

def format_number(num):
    try:
        return locale.format_string('%.2f', num, grouping=True)
    except Exception:
        return f"{num:.2f}"

# --- keyboards ---

def fiat_keyboard():
    kb = InlineKeyboardMarkup(row_width=3)
    for code, names in FIAT_CURRENCIES.items():
        kb.insert(InlineKeyboardButton(names["ru"], callback_data=f"fiat_{code}"))
    kb.add(InlineKeyboardButton("Назад", callback_data="menu"))
    return kb

def crypto_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    for coin_id, names in CRYPTO_CURRENCIES.items():
        kb.insert(InlineKeyboardButton(names["ru"], callback_data=f"crypto_{coin_id}"))
    kb.add(InlineKeyboardButton("Назад", callback_data="menu"))
    return kb

def chart_keyboard(typ, code):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📊 Неделя", callback_data=f"chart_{typ}_{code}_week"),
        InlineKeyboardButton("📊 Месяц", callback_data=f"chart_{typ}_{code}_month"),
    )
    kb.add(InlineKeyboardButton("Назад", callback_data=typ))
    return kb

# --- charts ---

async def generate_chart(typ: str, code: str, period: str):
    times, values = [], []
    current_rub = 0

    if typ == "crypto":
        days_map = {"week": "7", "month": "30"}
        interval_map = {"week": "daily", "month": "daily"}

        url = COIN_MARKET_CHART_API.format(id=code)
        params = {"vs_currency": "rub", "days": days_map.get(period, "7"),
                  "interval": interval_map.get(period, "daily")}
        data = await fetch_json(url, params)
        prices = data.get("prices", [])

        times = [datetime.datetime.fromtimestamp(p[0] / 1000) for p in prices]
        values = [p[1] for p in prices]

        current_data = await fetch_json(COIN_API, params={"ids": code, "vs_currencies": "rub"})
        current_rub = current_data.get(code, {}).get("rub", 0)

    elif typ == "fiat":
        days_count = {"week": 7, "month": 30}.get(period, 7)
        start_day = datetime.date.today() - datetime.timedelta(days=days_count - 1)
        for i in range(days_count):
            day = start_day + datetime.timedelta(days=i)
            url = f"https://www.cbr-xml-daily.ru/archive/{day.strftime('%Y/%m/%d')}/daily_json.js"
            try:
                data = await fetch_json(url)
            except:
                continue
            if not data:
                continue
            val = data.get("Valute", {}).get(code)
            if val:
                values.append(val["Value"])
                times.append(day)
        if values:
            current_rub = values[-1]

    plt.style.use("ggplot")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(times, values, marker='o', linestyle='-')
    ax.set_title(f"Курс {code.upper()} к рублю ({period})")
    ax.set_xlabel("Дата")
    ax.set_ylabel("Цена, ₽")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return buf, current_rub

@dp.callback_query_handler(lambda c: c.data.startswith("chart_"))
async def callback_chart(callback: types.CallbackQuery):
    await callback.answer()
    _, typ, code, period = callback.data.split("_")

    buf, current_rub = await generate_chart(typ, code, period)
    await callback.message.answer_photo(photo=InputFile(buf),
                                        caption=f"Текущий курс: {format_number(current_rub)} ₽")

# --- commands and menus ---

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("💵 Фиатные валюты", callback_data="fiat"),
        InlineKeyboardButton("₿ Криптовалюты", callback_data="crypto"),
    )
    await message.answer("👋 Привет! Я бот для показа курса валют и графиков.", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "fiat")
async def callback_fiat(callback: types.CallbackQuery):
    await callback.message.edit_text("Выбери фиатную валюту:", reply_markup=fiat_keyboard())

@dp.callback_query_handler(lambda c: c.data == "crypto")
async def callback_crypto(callback: types.CallbackQuery):
    await callback.message.edit_text("Выбери криптовалюту:", reply_markup=crypto_keyboard())

@dp.callback_query_handler(lambda c: c.data == "menu")
async def callback_menu(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("💵 Фиатные валюты", callback_data="fiat"),
        InlineKeyboardButton("₿ Криптовалюты", callback_data="crypto"),
    )
    await callback.message.edit_text("👋 Привет! Я бот для показа курса валют и графиков.", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data.startswith("fiat_"))
async def callback_fiat_currency(callback: types.CallbackQuery):
    code = callback.data[5:]
    rates = await get_fiat_rates()
    name = FIAT_CURRENCIES.get(code, {}).get("ru", code)
    rate = rates.get(code)
    if not rate:
        await callback.message.edit_text("Информация недоступна.")
        return
    msg = f"<b>{name}</b>: <b>{format_number(rate)}</b> ₽"
    await callback.message.edit_text(msg, reply_markup=chart_keyboard("fiat", code), parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data.startswith("crypto_"))
async def callback_crypto_currency(callback: types.CallbackQuery):
    coin_id = callback.data[7:]
    data = await fetch_json(COIN_API, params={"ids": coin_id, "vs_currencies": "rub,usd"})
    coin_data = data.get(coin_id, {})
    rub_rate = coin_data.get("rub")
    usd_rate = coin_data.get("usd")
    name = CRYPTO_CURRENCIES.get(coin_id, {}).get("ru", coin_id)
    if rub_rate is None or usd_rate is None:
        await callback.message.edit_text("Информация недоступна.")
        return
    msg = f"<b>{name}</b>: <b>{format_number(rub_rate)}</b> ₽ / <b>{format_number(usd_rate)}</b> $"
    await callback.message.edit_text(msg, reply_markup=chart_keyboard("crypto", coin_id), parse_mode="HTML")

# --- run ---

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
