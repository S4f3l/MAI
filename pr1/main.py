import logging
import time
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

BASE_URL = "https://online.stanford.edu/explore/page="

all_items = []
MAX_PAGES = 10
DELAY = 2

for page in range(MAX_PAGES):
    url = f"{BASE_URL}?page={page}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        logging.info(f"Страница {page} успешно загружена (статус {resp.status_code})")
    except requests.RequestException as e:
        logging.error(f"Страница {page}: ошибка {e}")
        continue

    soup = BeautifulSoup(resp.text, "html.parser")
    items = soup.select("div.course-card")

    if not items:
        logging.info(f"Страница {page} пуста — завершение.")
        break

    logging.info(f"Страница {page}: найдено {len(items)} записей.")
    for item in items:
        title = item.select_one("h3.course-program-card-title")
        desc = item.select_one("p.course-program-card-time-commitment")
        link = item.select_one("a.course-program-card-title")
        price = item.select_one("p.course-program-card-tuition")

        all_items.append({
            "title": title.get_text(strip=True) if title else None,
            "description": desc.get_text(strip=True) if desc else None,
            "link": link["href"] if link and link.has_attr("href") else None,
            "price": price.get_text(strip=True) if price else None,
        })

    time.sleep(DELAY)

logging.info(f"Сбор завершён. Всего записей: {len(all_items)}")
print(f"Всего собрано записей: {len(all_items)}")