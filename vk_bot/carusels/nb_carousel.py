import json
from vktools import Carousel

nb_sn_carousel = {
    "type": "carousel",
    "elements": [
        {
            "photo_id": "-221044024_457239042",
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
            "photo_id": "-221044024_457239024",
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
        },
        {
            "photo_id": "-221044024_457239043",
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
nb_sn_carousel = json.dumps(nb_sn_carousel, ensure_ascii=False).encode('utf-8')
nb_sn_carousel = str(nb_sn_carousel.decode('utf-8'))

nb_out_carousel = {
    "type": "carousel",
    "elements": [
        {
            "photo_id": "-221044024_457239041",
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
        }
    ]
}
nb_out_carousel = json.dumps(nb_out_carousel, ensure_ascii=False).encode('utf-8')
nb_out_carousel = str(nb_out_carousel.decode('utf-8'))