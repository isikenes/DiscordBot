import discord
import os
import requests
from keep_alive import keep_alive
import random

keep_alive()

token=os.environ.get('token')

# intents = discord.Intents.default()
# intents.guilds = True
# intents.guild_messages = True
# intents.messages = True
# intents.message_content = True
# intents.members = True

bot = discord.Bot()


def get_waifu():
    response = requests.get("https://api.waifu.pics/sfw/waifu")
    json_data = response.json()
    url = json_data["url"]
    return url


def get_nsfw():
    response = requests.get("https://api.waifu.pics/nsfw/waifu")
    json_data = response.json()
    url = json_data["url"]
    return url


def get_hava():
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 39.8152,
        "longitude": 30.5323,
        "current": ["temperature_2m", "weather_code"],
        "forecast_days": 1,
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    temperature_celsius = data["current"]["temperature_2m"]
    weather_condition = data["current"]["weather_code"]
    return temperature_celsius, weather_condition


def get_hava_metni(kod):
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
        99: "Gökgürültülü Fırtına: Şiddetli dolu",
    }
    return metin.get(kod, "Bilinmeyen")


def get_random_anime():
    anime_id = random.randint(1, 14000)
    response = requests.get(f"https://kitsu.io/api/edge/anime/{anime_id}")
    json_data = response.json()
    return json_data

def extract_data(json_data):
    try:
        title = json_data['data']['attributes']['canonicalTitle']
        poster_image = json_data['data']['attributes']['posterImage']['original']
        description = json_data['data']['attributes']['description']
        episode_count = json_data['data']['attributes']['episodeCount']
        rating_rank = json_data['data']['attributes']['ratingRank']
        return title, poster_image, description, episode_count, rating_rank
    except KeyError:
        return None
    
def get_anime_data(json_data):
    try:
        title = json_data['data'][0]['attributes']['canonicalTitle']
        poster_image = json_data['data'][0]['attributes']['posterImage']['original']
        description = json_data['data'][0]['attributes']['description']
        episode_count = json_data['data'][0]['attributes']['episodeCount']
        rating_rank = json_data['data'][0]['attributes']['ratingRank']
        return title, poster_image, description, episode_count, rating_rank
    except (KeyError, IndexError):
        return None

def process_data():
    while True:
        json_data = get_random_anime()
        data = extract_data(json_data)
        if data is not None:
            return data
        
def search_anime(query):
    url = f"https://kitsu.io/api/edge/anime?filter[text]={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

@bot.slash_command(description="Makima ile tanış")
async def makima(ctx):
    embed = discord.Embed(
        title=f"Emrediyorum, benimle anlaşma yapmak istediğini söyle {ctx.author.name}-kun!",
        color=0xE74C3C,
    )
    embed.set_image(url="https://pbs.twimg.com/media/EbDKI4gX0AUXzSO.jpg")

    await ctx.respond(embed=embed)


@bot.slash_command(description="Random waifu spawnla")
async def waifu(ctx):
    embed = discord.Embed(color=0xE74C3C)
    embed.set_image(url=get_waifu())

    await ctx.respond(embed=embed)


@bot.slash_command(description="Random waifu spawnla ama nsfw")
async def nsfw(ctx):
    if ctx.channel.nsfw:
        embed = discord.Embed(color=0xE74C3C)
        embed.set_image(url=get_nsfw())
        await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(
            description="Bu komut sadece NSFW kanallarında çalışır!", color=0xE74C3C
        )
        await ctx.respond(embed=embed)


@bot.slash_command(description="Avatarını göster")
async def avatar(ctx):
    embed = discord.Embed(color=0xE74C3C)
    embed.set_image(url=ctx.author.avatar.url)
    await ctx.respond(embed=embed)


@bot.slash_command(description="Eskişehir hava durumu")
async def hava(ctx):
    temperature_celsius, weather_condition = get_hava()
    hava = f"{temperature_celsius} C°\n{get_hava_metni(weather_condition)}"
    embed = discord.Embed(
        color=0xE74C3C, title="Eskişehir'de hava durumu:", description=hava
    )
    await ctx.respond(embed=embed)


@bot.slash_command(description="Botu üldürmek için sadece acil durumlarda kullanın")
async def kys(ctx):
    embed = discord.Embed(color=0xE74C3C, description="Sayonara...")
    await ctx.respond(embed=embed)
    await bot.close()


@bot.slash_command(description="Random veya ismi girilen animeyi getir")
async def anime(ctx, *, isim=None):

    if isim is None:
        title, poster_image, description, episode_count, rating_rank = process_data()
    else:
        if get_anime_data(search_anime(query=isim)) is None:
            errorEmbed=discord.Embed(
                color=0xE74C3C,
                description="Anime bulunamadı!"
            )
            await ctx.respond(embed=errorEmbed)
            return
        title, poster_image, description, episode_count, rating_rank = get_anime_data(search_anime(query=isim))

    embed=discord.Embed(
        color=0xE74C3C,
        title=title,
        description=description
    )
    embed.set_image(url=poster_image)
    embed.add_field(name="Episodes", value=episode_count, inline=True)
    embed.add_field(name="Ranked", value=rating_rank, inline=True)
    await ctx.respond(embed=embed)


bot.run(token=token)
