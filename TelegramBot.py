import telebot
from g4f.client import Client
import requests
from bs4 import BeautifulSoup
from textwrap import wrap

# Токен вашего бота Telegram
TOKEN = '7537760949:AAGht-uwsVuG4ZFDQpKI-I4pjwxjsfePH0U'
bot = telebot.TeleBot(TOKEN)


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


def summarize_url_content(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise ValueError(f'Не удалось получить доступ к URL: {url}. Код статуса: {r.status_code}')

    soup = BeautifulSoup(r.text, features="html.parser")
    prompt = 'Сделайте краткое содержание по этой странице. Выберите только самое важное, отвечая на том же языке, что и страница:\n\n'
    prompt += soup.text.strip()

    client = Client()
    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[{'role': 'user', 'content': prompt}]
    )
    summary = response.choices[0].message.content
    return summary


@bot.message_handler(regexp=r'^http(s)?://')
def handle_url(message):
    url = message.text
    try:
        summary = summarize_url_content(url)
        for line in wrap(summary, 65):
            bot.send_message(message.chat.id, line)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при обработке URL: {e}')


if __name__ == '__main__':
    bot.polling()
