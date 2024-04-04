import discord
import os
import io
import requests
from discord.ext import commands
from keep_alive import keep_alive

keep_alive()

token=os.environ.get('token')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()

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


@bot.command()
async def makima(ctx):
    await ctx.send(f"Emrediyorum, benimle anlaşma yapmak istediğini söyle {ctx.author.name}-kun!")
    await ctx.send("https://pbs.twimg.com/media/EbDKI4gX0AUXzSO.jpg")

@bot.command()
async def waifu(ctx):
    await ctx.send(getWaifu())

@bot.command()
async def nsfw(ctx):
    if ctx.channel.nsfw:
        await ctx.send(getNSFW())
    else:
        await ctx.send("Bu komut sadece NSFW kanallarında çalışır!")

@bot.command()
async def avatar(ctx):
    await ctx.send(ctx.author.avatar.url)

@bot.command()
async def hava(ctx):
    temperature_celsius, weather_condition = getHava()
    hava = f"Eskişehir'de hava durumu:\n{temperature_celsius} C°\n{getHavaMetni(weather_condition)}"
    await ctx.send(hava)

@bot.command()
async def kys(ctx):
    await ctx.send("Sayonara")
    await bot.close()

bot.run(token=token)