import telebot
TOKEN = '7537760949:AAGht-uwsVuG4ZFDQpKI-I4pjwxjsfePH0U'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, 'Привет! ' + message.from_user.first_name)
  bot.send_message(message.chat.id, message.text)

bot.polling()

from g4f.client import Client
import telebot
TOKEN = '7537760949:AAGht-uwsVuG4ZFDQpKI-I4pjwxjsfePH0U'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, 'Привет! ' + message.from_user.first_name)

@bot.message_handler(content_types=['text'])
def text(message):
  client = Client()
  response = client.chat.completions.create(
      model="gpt-4o",
      messages=[{"role": "user", "content": message.text}],
  )
  bot.send_message(message.chat.id, response.choices[0].message.content)

bot.polling()

from g4f.client import Client as G4FClient
from g4f import models
import requests
from bs4 import BeautifulSoup
from textwrap import wrap



url = 'https://www.cybersport.ru/tags/cs-go' # @param {type: "string"}

r = requests.get(url)
text = BeautifulSoup(r.text).text

prompt = 'Сделай краткое содержание по этой странице. Выбери только самое важное, отвечай на том же языке, что и страница:' # @param {type: "string"}
prompt += text

model = 'gpt-4o' # @param ['gpt-3.5-turbo', 'gpt-4o', 'gpt-4o-mini', 'gpt-4', 'gpt-4-turbo'] {allow-input: true}

def get_answer(text):
  i = 0
  while i < 10:
    client = G4FClient()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": text}],
    )
    res = response.choices[0].message.content
    i += 1

    if len(res) > 0 and 'Model' not in res and 'error' not in res and 'chat' not in res:
      return res
      break

if r.status_code == 200:
  answer = get_answer(prompt)
  for i in wrap(answer, 65):
    print(i)
else:
  print('Сайт не поддерживается')


