import json
from vktools import Carousel

j1_low_carousel = {
    "type": "carousel",
    "elements": [

        {
            "photo_id": "-221044024_457239018",
            "action": {
                "type": "open_photo"
            },
            "buttons": [
                {
                    "action": {
                        "type": "open_link",
                        "link": "https://vk.com/kixstock_manager",
                        "label": "Заказать",
                        "payload": "{}"
                }
            }]
        },

        {
            "photo_id": "-221044024_457239040",
            "action": {
                "type": "open_photo"
            },
            "buttons": [{
                "action": {
                    "type": "open_link",
                    "link": "https://vk.com/kixstock_manager",
                    "label": 'Заказать"',
                    "payload": "{}"
                }
            }]
        },
        {
            "photo_id": "-221044024_457239028",
            "action": {
                "type": "open_photo"
            },
            "buttons": [{
                "action": {
                    "type": "open_link",
                    "link": "https://vk.com/kixstock_manager",
                    "label": 'Заказать"',
                    "payload": "{}"
                }
            },

            ]
        }
    ]
}
j1_low_carousel = json.dumps(j1_low_carousel, ensure_ascii=False).encode('utf-8')
j1_low_carousel = str(j1_low_carousel.decode('utf-8'))

nike_und_carousel = {
    "type": "carousel",
    "elements": [
        {
            "photo_id": "-221044024_457239020",
            "action": {
                "type": "open_photo"
            },
            "buttons": [
                {
                    "action": {
                        "type": "open_link",
                        "link": "https://vk.com/kixstock_manager",
                        "label": "Заказать",
                        "payload": "{}"
                }
            }]
        },

        {
            "photo_id": "-221044024_457239023",
            "action": {
                "type": "open_photo"
            },
            "buttons": [{
                "action": {
                    "type": "open_link",
                    "link": "https://vk.com/kixstock_manager",
                    "label": "Заказать",
                    "payload": "{}"
                }
            }]
        }
    ]
}
nike_und_carousel = json.dumps(nike_und_carousel, ensure_ascii=False).encode('utf-8')
nike_und_carousel = str(nike_und_carousel.decode('utf-8'))

nike_out_carousel = {
    "type": "carousel",
    "elements": [

        {
            "photo_id": "-221044024_457239021",
            "action": {
                "type": "open_photo"
            },
            "buttons": [{
                "action": {
                    "type": "open_link",
                    "link": "https://vk.com/kixstock_manager",
                    "label": "Заказать",
                    "payload": "{}"
                }
            }
            ]
        }
    ]
}
nike_out_carousel = json.dumps(nike_out_carousel, ensure_ascii=False).encode('utf-8')
nike_out_carousel = str(nike_out_carousel.decode('utf-8'))
