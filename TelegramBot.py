import telebot
from g4f.client import Client
import requests
from bs4 import BeautifulSoup
from textwrap import wrap
import sqlite3
from datetime import datetime

# Токен вашего бота Telegram
TOKEN = '7537760949:AAGht-uwsVuG4ZFDQpKI-I4pjwxjsfePH0U'
bot = telebot.TeleBot(TOKEN)

# Подключение к базе данных SQLite
conn = sqlite3.connect('history.db')
cursor = conn.cursor()

# Создание таблицы history, если её ещё нет
cursor.execute('''
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет! {message.from_user.first_name}')


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        client = Client()
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[{'role': 'user', 'content': message.text}]
        )
        bot.send_message(message.chat.id, response.choices[0].message.content)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')


def get_full_page_content(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise ValueError(f'Не удалось получить доступ к URL: {url}. Код статуса: {r.status_code}')

    soup = BeautifulSoup(r.text, features="html.parser")
    full_content = soup.text.strip()
    return full_content


def save_to_history(url, content):
    cursor.execute("INSERT INTO history (url, content) VALUES (?, ?)", (url, content))
    conn.commit()


def fetch_from_history(url):
    cursor.execute("SELECT content, timestamp FROM history WHERE url = ? ORDER BY timestamp DESC LIMIT 1", (url,))
    result = cursor.fetchone()
    return result[0], result[1] if result else (None, None)


@bot.message_handler(regexp=r'^http(s)?://')
def handle_url(message):
    url = message.text
    try:
        fresh_content = get_full_page_content(url)
        old_content, old_timestamp = fetch_from_history(url)

        if old_content is None or fresh_content != old_content:
            save_to_history(url, fresh_content)
            content = fresh_content
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            content = old_content
            timestamp = old_timestamp

        for line in wrap(content, 4096):
            bot.send_message(message.chat.id, line)
        bot.send_message(message.chat.id, f'Информация актуальна на: {timestamp}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при обработке URL: {e}')


if __name__ == '__main__':
    bot.polling()
