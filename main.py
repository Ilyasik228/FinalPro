# Импорт необходимых модулей
import sqlite3  # Модуль для работы с базой данных SQLite
import requests  # Модуль для выполнения HTTP-запросов
from bs4 import BeautifulSoup  # Модуль для парсинга HTML-кода

# Создание подключения к базе данных SQLite и создание курсора
conn = sqlite3.connect('internet_database.db')  # Подключение к базе данных или создание новой, если её нет
cursor = conn.cursor()  # Создание курсора для выполнения SQL-запросов

# Создание таблицы 'pages', если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS pages
                (url TEXT PRIMARY KEY, content TEXT)''')

# Функция для добавления сайта в базу данных
def add_site_to_database(url):
    try:
        # Получение содержимого страницы
        response = requests.get(url)  # Запрос к странице по заданному URL
        soup = BeautifulSoup(response.text, 'html.parser')  # Парсинг HTML-кода страницы
        content = '\n'.join([p.text for p in soup.find_all('p')])  # Получение текста абзацев

        # Вставка данных в таблицу
        cursor.execute("INSERT OR REPLACE INTO pages (url, content) VALUES (?, ?)", (url, content))
        conn.commit()  # Применение изменений к базе данных
        print(f"Сайт {url} успешно добавлен в базу данных.")
    except Exception as e:
        print(f"Ошибка при добавлении сайта {url} в базу данных:", e)

# Функция для очистки базы данных
def clear_database():
    cursor.execute("DELETE FROM pages")  # Удаление всех записей из таблицы 'pages'
    conn.commit()  # Применение изменений к базе данных
    print("База данных успешно очищена.")

# Функция для поиска информации на страницах
def search_database(query):
    cursor.execute("SELECT url, content FROM pages")  # Выборка всех записей из таблицы 'pages'
    results = cursor.fetchall()  # Получение всех результатов
    for url, content in results:
        if query.lower() in content.lower():  # Поиск по содержимому страниц
            print(f"Сайт: {url}")  # Вывод URL найденной страницы
            print("Текст сайта:")
            print(content)  # Вывод текста страницы
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

# Закрытие соединения с базой данных
conn.close()
