import telebot
import requests
from tokens import yandexToken,telegramToken,wetherToken
import xmltodict, json

def getWether(longitude,latitude):
	URL = "http://api.weatherapi.com/v1/current.json"	
	PARAMS =  {"q":",".join([longitude,latitude]),"key":wetherToken}
	r = requests.get(url=URL,params=PARAMS)
	data = r.json()
	return data

def getLocation(city):
	URL = "https://geocode-maps.yandex.ru/1.x"
	PARAMS = {"apikey":yandexToken,"geocode":city,"lang":"ru_RU"}
	r = requests.get(url = URL, params= PARAMS)
	data = xmltodict.parse(r.content)
	latitude, longitude  = data["ymaps"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()
	return getWether(longitude,latitude)
	
bot = telebot.TeleBot(telegramToken, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет, напиши название города и я подскажу погоду")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	try:
		wetherData = getLocation(message.text)["current"]
		response = "Температура: {temp_c} °C\nСкорость ветра: {wind_kph} км/ч\nВлажность: {humidity}%\nОблачность: {cloud}%\nЧувствуется как: {feelslike_c}°C\n".format(**wetherData)
	except:
		response="Что-то пошло не так, попробуй заново"
	bot.reply_to(message, response)

bot.infinity_polling()
