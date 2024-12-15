import telebot
from g4f.client import Client

# Токен вашего бота
TOKEN = '7537760949:AAGht-uwsVuG4ZFDQpKI-I4pjwxjsfePH0U'
bot = telebot.TeleBot(TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет! {message.from_user.first_name}')


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    try:
        client = Client()
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[{'role': 'user', 'content': message.text}]
        )

        bot.send_message(message.chat.id, response.choices[0].message.content)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")


# Запуск бота
bot.polling()

import requests
from bs4 import BeautifulSoup
from textwrap import wrap
from g4f.client import Client as G4FClient
from g4f import models

# URL страницы для анализа
url = 'https://www.counter-strike.net/'

# Получение содержимого страницы
try:
    response = requests.get(url)
except requests.exceptions.RequestException as e:
    print(f"Ошибка при получении данных с сайта: {e}")
    exit()

if response.status_code != 200:
    print("Не удалось получить данные с сайта.")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')
page_content = soup.text

# Подготовка запроса к модели
prompt = 'Сделайте краткое содержание по этой странице. Выберите только самое важное, отвечая на том же языке, что и страница:'
prompt += page_content

# Выбор модели
model = 'gpt-4-turbo'

client = G4FClient()
response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": prompt}]
)

result = response.choices[0].message.content

for line in wrap(result, 65):
    print(line)
