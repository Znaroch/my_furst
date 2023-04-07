import telebot
import requests
import json
from config import TOKEN, keys
from classes import ConvertException, ConvertValues

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в формате: <имя валюты>\
    <в какую валюту хотите перевести>\
    <количество переводимой валюты>.\nНапример: евро рубль 100 \nСписок валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)



@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertException('Должно быть написано три параметра, смотри описание!')
        quote, base, amount = values
        total_base = ConvertValues.convert(quote, base, amount)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось выполнить команду\n{e}')
    else:
        bot.reply_to(message, f'Стоимость покупки {keys[base]} за {amount} {keys[quote]}: {total_base} {keys[base]}')



bot.polling()



