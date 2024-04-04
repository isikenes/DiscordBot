import discord
import os
import time
import random
import aiohttp
import io
import requests

token=os.environ.get('token')

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")
    

iblisler=['Tilki İblisi','Gelecek İblisi','Yılan İblisi','Zombi İblisi','Silah İblisi']


def getWaifu():
    response = requests.get("https://api.waifu.pics/sfw/waifu")
    json_data = response.json()
    url = json_data['url']
    return url


def getNSFW():
    response = requests.get("https://api.waifu.pics/nsfw/waifu")
    json_data = response.json()
    url = json_data['url']
    return url

def getHava():
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 39.8152,
        "longitude": 30.5323,
        "current": ["temperature_2m", "weather_code"],
	    "forecast_days": 1
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    temperature_celsius = data["current"]["temperature_2m"]
    weather_condition = data["current"]["weather_code"]
    return temperature_celsius, weather_condition

def getHavaMetni(kod):
    metin = {
        0: "Açık gökyüzü",
        1: "Genellikle açık gökyüzü",
        2: "Parçalı bulutlu",
        3: "Hava kapalı",
        45: "Sis",
        48: "Buzlanma ve sis",
        51: "Çiseleme: Hafif yoğunluk",
        53: "Çiseleme: Orta yoğunluk",
        55: "Çiseleme: Yoğun",
        56: "Donan Çiseleme: Hafif yoğunluk",
        57: "Donan Çiseleme: Yoğun",
        61: "Yağmur: Hafif yoğunluk",
        63: "Yağmur: Orta yoğunluk",
        65: "Yağmur: Şiddetli yoğunluk",
        66: "Donan Yağmur: Hafif yoğunluk",
        67: "Donan Yağmur: Şiddetli yoğunluk",
        71: "Kar Yağışı: Hafif yoğunluk",
        73: "Kar Yağışı: Orta yoğunluk",
        75: "Kar Yağışı: Şiddetli yoğunluk",
        77: "Kar Taneleri",
        80: "Yağmur Yağışı: Hafif yoğunluk",
        81: "Yağmur Yağışı: Orta yoğunluk",
        82: "Yağmur Yağışı: Şiddetli yoğunluk",
        85: "Kar Yağışı: Hafif yoğunluk",
        86: "Kar Yağışı: Şiddetli yoğunluk",
        95: "Gökgürültülü Fırtına: Hafif veya orta yoğunluk",
        96: "Gökgürültülü Fırtına: Hafif dolu",
        99: "Gökgürültülü Fırtına: Şiddetli dolu"
    }
    return metin.get(kod, "Bilinmeyen")


@client.event
async def on_message(msg):
    if msg.author!=client.user:
        if msg.content.lower().startswith("/makima"):
            await msg.channel.send(f"Emrediyorum, benimle anlaşma yapmak istediğini söyle {msg.author.display_name}-kun.")
            url = "https://pbs.twimg.com/media/EbDKI4gX0AUXzSO.jpg"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    img = await resp.read()
                    with io.BytesIO(img) as file:
                        await msg.channel.send(file=discord.File(file, "makima.png"))
            
        if msg.content.lower().startswith("seninle anlaşma yapmak istiyorum"):
            await msg.channel.send(f"Makima yetenek etkinleştirdi: şunların yeteneklerini kullan. {msg.author.display_name}-kun'un {random.choice(iblisler)} ile ölene kadar geçerli anlaşması.")

    if msg.content.startswith("/waifu"):
        await msg.channel.send(getWaifu())

    if msg.content.startswith("/nsfw"):
        if(msg.channel.nsfw):
            await msg.channel.send(getNSFW())

    if msg.content.startswith("/avatar"):
        await msg.channel.send(msg.author.avatar.url)

    if msg.content.startswith("/hava"):
        temperature_celsius, weather_condition = getHava()
        hava=f"Eskişehir'de hava durumu:\n{temperature_celsius} C°\n{getHavaMetni(weather_condition)}"
        await msg.channel.send(hava)


client.run(token)