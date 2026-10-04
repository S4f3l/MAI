import random
import os
import pandas as pd
from faker import Faker

# Инициализация Faker с русской локализацией
fake = Faker('ru_RU')
Faker.seed(42)
random.seed(42)

# Справочники
должности = [
    "Менеджер", "Старший менеджер", "Специалист", "Ведущий специалист",
    "Инженер", "Старший инженер", "Бухгалтер", "Экономист", "Аналитик",
    "Программист", "Системный администратор", "HR-специалист",
    "Юрист", "Логист", "Маркетолог", "Дизайнер", "Руководитель отдела",
    "Заместитель директора", "Секретарь", "Курьер"
]

отделы = [
    "Отдел продаж", "Отдел маркетинга", "Бухгалтерия", "Финансовый отдел",
    "IT-отдел", "Отдел кадров", "Юридический отдел", "Логистика",
    "Отдел закупок", "Производственный отдел", "Отдел аналитики",
    "Административный отдел", "Отдел разработки", "Служба поддержки"
]

# Генерация данных
N = 2000
data = {
    "Табельный номер": [f"{i:05}" for i in range(1, N + 1)],
    "ФИО": [fake.name() for _ in range(N)],
    "Должность": [random.choice(должности) for _ in range(N)],
    "Отдел": [random.choice(отделы) for _ in range(N)],
}

df = pd.DataFrame(data)

# Сохранение
df.to_excel("сотрудники.xlsx", index=False)
df.to_csv("сотрудники.csv", index=False, encoding="utf-8-sig")

print(f"Создано {len(df)} строк")
print(df.head(10))
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
df.to_excel(os.path.join(desktop, "сотрудники.xlsx"), index=False)
df.to_csv(os.path.join(desktop, "сотрудники.csv"), index=False, encoding="utf-8-sig")