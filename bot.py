import discord
from discord.ext import commands
import os
import requests
from keep_alive import keep_alive
import random as rand
from pytube import YouTube
from elevenlabs import Voice
from elevenlabs.client import ElevenLabs
import io
from googleapiclient.discovery import build

keep_alive()

token = os.environ.get("token")
gkey = os.environ.get("gkey")
cseid = os.environ.get("cseid")
eleven_key=os.environ.get("eleven_key")

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
embedColor = 0xE74C3C
client=ElevenLabs(
    api_key=eleven_key
)
VOICE_TYPE_MAPPING = {
    "kiz1": "qKRN53Lk573XAhUO8SnB",
    "kiz2": "LbzRMxs5MRauwrHmFCLl",
    "chaddarby": "yrDMz47qnZxD5j7m1DcV"
}

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
    anime_id = rand.randint(1, 14000)
    response = requests.get(f"https://kitsu.io/api/edge/anime/{anime_id}")
    json_data = response.json()
    return json_data


def extract_data(json_data):
    try:
        title = json_data["data"]["attributes"]["canonicalTitle"]
        poster_image = json_data["data"]["attributes"]["posterImage"]["original"]
        description = json_data["data"]["attributes"]["description"]
        episode_count = json_data["data"]["attributes"]["episodeCount"]
        rating_rank = json_data["data"]["attributes"]["ratingRank"]
        return title, poster_image, description, episode_count, rating_rank
    except KeyError:
        return None


def get_anime_data(json_data):
    try:
        title = json_data["data"][0]["attributes"]["canonicalTitle"]
        poster_image = json_data["data"][0]["attributes"]["posterImage"]["original"]
        description = json_data["data"][0]["attributes"]["description"]
        episode_count = json_data["data"][0]["attributes"]["episodeCount"]
        rating_rank = json_data["data"][0]["attributes"]["ratingRank"]
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


def search_image(query):
    try:
        service = build("customsearch", "v1", developerKey=gkey)
        res = service.cse().list(q=query, cx=cseid, searchType="image", num=1).execute()
        if "items" in res:
            return res["items"][0]["link"]
    except:
        return None


def get_card(query):
    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?fname={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            title = data["data"][0]["name"]
            desc = data["data"][0]["desc"]
            tip = data["data"][0]["type"]
            race = data["data"][0]["race"]
            img = data["data"][0]["card_images"][0]["image_url"]
            return title, desc, tip, race, img
        except:
            return None
    else:
        return None
    
def generated_download_link(youtube_url):
    try:
        yt = YouTube(youtube_url)
        stream = yt.streams.get_highest_resolution()
        download_link = stream.url
        return download_link
    except Exception as e:
        return None


@bot.command(name="makima", description="Makima ile tanış")
async def makima(ctx):
    embed = discord.Embed(
        title=f"Emrediyorum, benimle anlaşma yapmak istediğini söyle {ctx.author.name}-kun!",
        color=embedColor,
    )
    embed.set_image(url="https://pbs.twimg.com/media/EbDKI4gX0AUXzSO.jpg")

    await ctx.send(embed=embed)


@bot.command(name="waifu", description="Random waifu spawnla")
async def waifu(ctx):
    embed = discord.Embed(color=embedColor)
    embed.set_image(url=get_waifu())

    await ctx.send(embed=embed)


@bot.command(name="nsfw", description="Random waifu spawnla ama nsfw")
async def nsfw(ctx):
    if ctx.channel.nsfw:
        embed = discord.Embed(color=embedColor)
        embed.set_image(url=get_nsfw())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            description="Bu komut sadece NSFW kanallarında çalışır!", color=embedColor
        )
        await ctx.send(embed=embed)


@bot.command(name="avatar", description="Avatarını gösterir")
async def avatar(ctx):
    embed = discord.Embed(color=embedColor)
    embed.set_image(url=ctx.author.avatar.url)
    await ctx.send(embed=embed)


@bot.command(name="hava", description="Eskişehir hava durumu")
async def hava(ctx):
    temperature_celsius, weather_condition = get_hava()
    hava = f"{temperature_celsius} C°\n{get_hava_metni(weather_condition)}"
    embed = discord.Embed(
        color=embedColor, title="Eskişehir'de hava durumu:", description=hava
    )
    await ctx.send(embed=embed)


@bot.command(
    name="kys", description="Botu üldürmek için sadece acil durumlarda kullanın"
)
async def kys(ctx):
    if ctx.author.name == "_vault_hunter_":
        embed = discord.Embed(color=embedColor, description="Sayonara...")
        await ctx.send(embed=embed)
        await bot.close()
    else:
        embed = discord.Embed(color=embedColor, description="Botu üldürme iznin yok!")
        await ctx.send(embed=embed)


@bot.command(
    name="anime", description="Rastgele bir anime veya ismi girilen animeyi getir"
)
async def anime(ctx, *, isim=None):

    if isim is None:
        title, poster_image, description, episode_count, rating_rank = process_data()
    else:
        if get_anime_data(search_anime(query=isim)) is None:
            errorEmbed = discord.Embed(
                color=embedColor, description="Anime bulunamadı!"
            )
            await ctx.send(embed=errorEmbed)
            return
        title, poster_image, description, episode_count, rating_rank = get_anime_data(
            search_anime(query=isim)
        )

    embed = discord.Embed(color=embedColor, title=title, description=description)
    embed.set_image(url=poster_image)
    embed.add_field(name="Episodes", value=episode_count, inline=True)
    embed.add_field(name="Ranked", value=rating_rank, inline=True)
    await ctx.send(embed=embed)


@bot.command(name="random", description="Seçeneklerden rastgele birini seçer")
async def random(ctx, *, secenekler: str = None):

    if secenekler is None:
        errorEmbed = discord.Embed(
            color=embedColor, description="En az 2 seçenek girin!"
        )
        await ctx.send(embed=errorEmbed)
        return

    s = secenekler.split()
    s = list(set(s))

    if len(s) < 2:
        errorEmbed = discord.Embed(
            color=embedColor, description="En az 2 seçenek girin!"
        )
        await ctx.send(embed=errorEmbed)
        return

    sec = rand.choice(s)
    embed = discord.Embed(
        color=embedColor, title="Seçtiğim seçenek: ", description=f"{sec.upper()}"
    )
    embed.set_image(
        url="https://media1.tenor.com/m/gq8idcUwAk0AAAAd/chainsaw-man-makima-hands-chainsaw-man.gif"
    )
    await ctx.send(embed=embed)


@bot.command(name="help", description="Komutları gösterir")
async def help(ctx):
    embed = discord.Embed(title="Komut listesi", color=embedColor)

    for command in bot.commands:
        embed.add_field(
            name=f"Komut: {command.name}",
            value=f"İşlevi: {command.description}",
            inline=False,
        )

    await ctx.send(embed=embed)


@bot.command(name="foto", description="Görsel arama yapar")
async def foto(ctx, *, query=None):
    if query is None:
        errorEmbed = discord.Embed(
            color=embedColor, description="Görsel arama yapmak için sorgu girmen gerek!"
        )
        await ctx.send(embed=errorEmbed)

    image_url = search_image(query)
    if image_url:
        embed = discord.Embed(color=embedColor)
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        errorEmbed = discord.Embed(color=embedColor, description="Görsel bulunamadı!")
        await ctx.send(embed=errorEmbed)


@bot.command(name="yugioh", description="Girilen Yugioh kartının bilgilerini gösterir")
async def yugioh(ctx, *, name=None):
    if name is None:
        errorEmbed = discord.Embed(
            color=embedColor, description="Kart bilgisi girilmedi!"
        )
        await ctx.send(embed=errorEmbed)
        return

    if get_card(name) is None:
        errorEmbed = discord.Embed(color=embedColor, description="Kart bulunamadı!")
        await ctx.send(embed=errorEmbed)
        return

    title, desc, tip, race, img = get_card(name)
    embed = discord.Embed(color=embedColor, title=title, description=desc)
    embed.add_field(name="Type: ", value=tip, inline=True)
    embed.add_field(name="Race: ", value=race, inline=True)
    embed.set_image(url=img)
    await ctx.send(embed=embed)


@bot.command(name="indir", description="Girilen youtube videosunun indirme linkini atar")
async def indir(ctx, youtube_url: str):
    if youtube_url is None:
        errorEmbed = discord.Embed(
            color=embedColor, description="Youtube linki girilmedi!"
        )
        await ctx.send(embed=errorEmbed)
        return
    
    await ctx.defer()
    download_link = generated_download_link(youtube_url)
    if download_link is None:
        errorEmbed = discord.Embed(
            color=embedColor, description="Youtube linki bulunamadı!"
        )
        await ctx.send(embed=errorEmbed)
        return
    
    embed = discord.Embed(color=embedColor,title="İndir", url=download_link)
    await ctx.send(embed=embed)



@bot.command(name="ses", description="Metni sese dönüştür")
async def ses(ctx, voice_type: str, *text: str):
        
    await ctx.defer()
    voice_type = voice_type.lower()
    if voice_type not in VOICE_TYPE_MAPPING:
        errorEmbed = discord.Embed(
            color=embedColor, description=f"Ses tipi bulunamadı! Ses tipleri: {VOICE_TYPE_MAPPING.keys}"
        )
        await ctx.send(embed=errorEmbed)
        return
    
    if text is None:
        errorEmbed = discord.Embed(
            color=embedColor, description="Metin girilmedi!"
        )
        await ctx.send(embed=errorEmbed)
        return

    selected_voice_id = VOICE_TYPE_MAPPING[voice_type]

    message = " ".join(text)

    output = client.generate(
        text=message,
        voice=Voice(voice_id=selected_voice_id),
        model="eleven_multilingual_v2",
    )

    output_bytes = b"".join(output)
    await ctx.send(file=discord.File(io.BytesIO(output_bytes), filename="ses.mp3"))


bot.run(token=token)
