import sqlite3
import requests
from bs4 import BeautifulSoup

# Создаем подключение к базе данных
conn = sqlite3.connect('internet_database.db')
cursor = conn.cursor()

# Создаем таблицу, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS pages
                (url TEXT PRIMARY KEY, content TEXT)''')

# Функция для добавления сайта в базу данных
def add_site_to_database(url):
    try:
        # Получаем содержимое страницы
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = '\n'.join([p.text for p in soup.find_all('p')])

        # Вставляем данные в таблицу
        cursor.execute("INSERT OR REPLACE INTO pages (url, content) VALUES (?, ?)", (url, content))
        conn.commit()  # Применяем изменения к базе данных
        print(f"Сайт {url} успешно добавлен в базу данных.")
    except Exception as e:
        print(f"Ошибка при добавлении сайта {url} в базу данных:", e)

# Функция для очистки базы данных
def clear_database():
    cursor.execute("DELETE FROM pages")
    conn.commit()  # Применяем изменения к базе данных
    print("База данных успешно очищена.")

# Функция для поиска информации на страницах
def search_database(query):
    cursor.execute("SELECT url, content FROM pages")
    results = cursor.fetchall()
    for url, content in results:
        if query.lower() in content.lower():
            print(f"Сайт: {url}")
            print("Текст сайта:")
            print(content)
            return
    print("Информация не найдена в базе данных :(")

# Интерфейс для взаимодействия с пользователем
while True:
    print("\nМеню:")
    print("1. Добавить сайт в базу данных")
    print("2. Очистить базу данных")
    print("3. Поиск информации на страницах")
    print("4. Выйти")

    choice = input("Выберите действие: ")

    if choice == "1":
        url = input("Введите URL сайта для добавления в базу данных: ")
        add_site_to_database(url)
    elif choice == "2":
        clear_database()
    elif choice == "3":
        query = input("Введите информацию для поиска: ")
        search_database(query)
    elif choice == "4":
        print("До свидания!")
        break
    else:
        print("Неверный выбор. Пожалуйста, выберите действие из списка.")

# Закрываем подключение к базе данных
conn.close()