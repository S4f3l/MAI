import json
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vktools import Keyboard, ButtonColor, Text, Carousel, Element

import time
import requests
import keyboard
import itertools

from carusels.nike_x_jordan import j1_low_carousel, nike_und_carousel, nike_out_carousel
from carusels.nb_carousel import nb_sn_carousel, nb_out_carousel


session = vk_api.VkApi(token="vk1.a.hPuS1qO5vF0gMSmK-xgtnLpvYYuNbFKwMPN_yiqkL7oDQrup_FosGjy23MjOu-FGl0JK5bQTrindu-hBfBRl0LXbQMhGkGfZRVecso36bTVsCbpKMzGhVi4T8_10mh-sa2ftF77kD1pRExchzJ7gi3l1LvWSUkf6Ng33f0J1-8O3zIQB37C6cDTFD0CGq1gmxUY03yiDIw1u6L__WJJjzQ")

def send_message(user_id, message, keyboard=None, carousel=None):
    post = {
        "user_id": user_id,
        "message": message,
        "random_id": 0,
        "template": carousel
    }

    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()

    session.method("messages.send", post)


for event in VkLongPoll(session).listen():  # перебирем объекты событий
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:  # сообщение адресовано боту
        text = event.text.lower()  # перевод в нижный регистр
        user_id = event.user_id

        if text == "начать":
            keyboard = VkKeyboard()
            keyboard.add_button("Каталог", VkKeyboardColor.PRIMARY)
            keyboard.add_button("Ответы на основные вопросы", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("Узнать курс юаня к рублю", VkKeyboardColor.PRIMARY)
            # keyboard.add_button("Рассчитать стоимость", VkKeyboardColor.PRIMARY)
            send_message(user_id, "Приветствуем в онлайн-магазине!", keyboard)

        if text == "главное меню":
            keyboard = VkKeyboard()
            keyboard.add_button("Каталог", VkKeyboardColor.PRIMARY)
            keyboard.add_button("Ответы на основные вопросы", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("Узнать курс юаня к рублю", VkKeyboardColor.PRIMARY)
            send_message(user_id, "Вы вернулись в главное меню", keyboard)

        if text == "назад":
            keyboard = VkKeyboard()
            keyboard.add_button("Jordan x Nike", VkKeyboardColor.PRIMARY)
            keyboard.add_button("New Balance", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("Главное меню", VkKeyboardColor.NEGATIVE)
            send_message(user_id, "Вы перешли к выбору бренда", keyboard)

        if text == "узнать курс юаня к рублю":
            keyboard = VkKeyboard()
            send_message(user_id, "Наш курс: 1 юань = 12.3 рубля")

        # if text == "рассчитать стоимость":
        #     keyboard = VkKeyboard()
        #     send_message(user_id, "Введите стоимость")
        #
        # if text.isnumeric():
        #     value = int(text)
        #     result = value * 12.3 + 2300
        #     response = f"Результат: {result}"
        # else:
        #     send_message(user_id, "e7e626")

        if text == "ответы на основные вопросы":
            keyboard = VkKeyboard()
            keyboard.add_button("Какие сроки доставки?", VkKeyboardColor.PRIMARY)
            keyboard.add_button("Как расчитать стоимость товара?", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("Как забрать свой заказ?", VkKeyboardColor.PRIMARY)
            keyboard.add_button("Оригинал?", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("Главное меню", VkKeyboardColor.NEGATIVE)
            send_message(user_id, "Выберите вопрос", keyboard)

        if text == "какие сроки доставки?":
            keyboard = VkKeyboard()
            send_message(user_id, "Доставка в среднем занимает от 20 до 25 дней.\n\n"
                         "Доставка кастомных товаров обычно дольше.")

        if text == "как расчитать стоимость товара?":
            keyboard = VkKeyboard()
            send_message(user_id, "Рассчитать стоимость вы можете в нашем боте. Или при помощи формулы: стоимость в юанях * курс + 1300 (доставка) + 1000 (комиссия).\n\n"
                                      "При оптовом заказе от 10 позиций цена меняется.")

        if text == "как забрать свой заказ?":
            keyboard = VkKeyboard()
            send_message(user_id, "Забрать заказ вы можете либо самовывозом с нашего склада, либо на пункте выдачи сдек.\n\n"
                         "Перед получением заказа вам нужно написать в службу поддержки.")

        if text == "оригинал?":
            keyboard = VkKeyboard()
            send_message(user_id, "Да, все вещи проходят тщательную проверку на оригинальность на платформе POIZON.")

        if text == "каталог":
            keyboard = VkKeyboard()
            keyboard.add_button("Jordan x Nike", VkKeyboardColor.PRIMARY)
            keyboard.add_button("New Balance", VkKeyboardColor.PRIMARY)
            send_message(user_id, "Выберите бренд", keyboard)

        if text == "jordan x nike":
            keyboard = VkKeyboard()
            keyboard.add_button("Кроссовки Jordan x Nike", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("Одежда Jordan x Nike", VkKeyboardColor.PRIMARY)
            keyboard.add_button("Аксессуары Jordan x Nike", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("Главное меню", VkKeyboardColor.NEGATIVE)
            send_message(user_id, "Что вас интересует?", keyboard)

        if text == "кроссовки jordan x nike":
            send_message(user_id, "Наш ассортимент\n"
                                  "Если не нашли интресующий товар, напишите менеджеру, посмотрим на наличие!", carousel=j1_low_carousel)

        if text == "одежда jordan x nike":
            keyboard = VkKeyboard()
            keyboard.add_button("Верхняя одежда Jordan x Nike", VkKeyboardColor.PRIMARY)
            keyboard.add_button("Нижняя одежда Jordan x Nike", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
            send_message(user_id, "Что вас интересует?", keyboard)

        if text == "верхняя одежда jordan x nike":
            send_message(user_id, "Наш ассортимент\n"
                                  "Если не нашли интресующий товар, напишите менеджеру, посмотрим на наличие!", carousel=nike_out_carousel)


        if text == "нижняя одежда jordan x nike":
            send_message(user_id, "Наш ассортимент\n"
                                  "Если не нашли интресующий товар, напишите менеджеру, посмотрим на наличие!", carousel=nike_und_carousel)

        if text == "new balance":
            keyboard = VkKeyboard()
            keyboard.add_button("Кроссовки NB", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("Одежда NB", VkKeyboardColor.PRIMARY)
            keyboard.add_button("Аксессуары NB", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("", VkKeyboardColor.NEGATIVE)
            send_message(user_id, "Что вас интересует?", keyboard)

        if text == "кроссовки nb":
            keyboard = VkKeyboard()
            keyboard.add_openlink_button("Товары", "https://vk.com/market-220253762?screen=group")
            send_message(user_id, "Наш ассортимент\n"
                                  "Если не нашли интресующий товар, напишите менеджеру, посмотрим на наличие!",
                         carousel=nb_sn_carousel)

        if text == "одежда nb":
            keyboard = VkKeyboard()
            keyboard.add_button("Верхняя одежда NB", VkKeyboardColor.PRIMARY)
            keyboard.add_button("Нижняя одежда NB", VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button("Назад", VkKeyboardColor.NEGATIVE)
            send_message(user_id, "Что вас интересует?", keyboard)

        if text == "верхняя одежда nb":
            send_message(user_id, "Наш ассортимент\n"
                                  "Если не нашли интресующий товар, напишите менеджеру, посмотрим на наличие!",
                         carousel=nb_out_carousel)








