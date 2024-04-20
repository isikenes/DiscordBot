import discord
from discord.ext import commands
import os
import requests
from keep_alive import keep_alive
import random as rand
from pytube import YouTube
from googleapiclient.discovery import build

keep_alive()

token = os.environ.get("token")
gkey = os.environ.get("gkey")
cseid = os.environ.get("cseid")
wkey=os.environ.get("wkey")

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
embedColor = 0xE74C3C

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


def get_hava(city):
    try:
        base_url = "https://api.weatherapi.com/v1/current.json"
        params = {
            "key":wkey,
            "q":city
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        location=data["location"]["name"]
        temp=data["current"]["temp_c"]
        humidity=data["current"]["humidity"]
        wind=data["current"]["wind_kph"]
        condition=data["current"]["condition"]["text"]
        image_url="http:"+data["current"]["condition"]["icon"]
        return location, temp,humidity,wind,condition,image_url
    except:
        return None


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


@bot.command(name="hava", description="Girilen şehrin hava durumunu gösterir")
async def hava(ctx, *, city:str=None):
    if city is None:
        errorEmbed = discord.Embed(
            color=embedColor, description="Şehir ismi girin!"
        )
        await ctx.send(embed=errorEmbed)
        return
    
    if get_hava(city=city) is None:
        errorEmbed = discord.Embed(
            color=embedColor, description="Şehir bulunamadı!"
        )
        await ctx.send(embed=errorEmbed)
        return

    location, temp,humidity,wind,condition,image_url=get_hava(city=city)
    
    embed = discord.Embed(
        color=embedColor, title=f"{location} hava durumu:", description=f"{condition}, {temp} C°"
    )
    embed.add_field(name="Nem: ", value=humidity, inline=True)
    embed.add_field(name="Rüzgar: ", value=f"{wind} km/h", inline=True)
    embed.set_thumbnail(url=image_url)
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
async def anime(ctx, *, isim:str=None):

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

bot.run(token=token)
