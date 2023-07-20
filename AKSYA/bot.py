from asyncio import streams
from audioop import add
from cgitb import text
from http import client
from lib2to3.pgen2 import token
from optparse import Option
from pydoc import describe
from sqlite3 import connect
from token import SLASH
from tokenize import maybe

from typing import Any
from unicodedata import name
from webbrowser import get
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.utils import utcnow
from nextcord.utils import get
from translate import Translator
import random
import requests
from PIL import Image, ImageFont, ImageDraw
import youtube_dl
import time
import timeago as timesince
import datetime
import calendar
start_time = utcnow()

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="?", intents=intents)
bot.remove_command("help")

def some_function():
    "This function does nothing"
    return None


def date(
    target,
    clock: bool = True,
    seconds: bool = False,
    ago: bool = False,
    only_ago: bool = False,
    raw: bool = False,
):
    if isinstance(target, int) or isinstance(target, float):
        target = datetime.datetime.utcfromtimestamp(target)

    if raw:
        if clock:
            timestamp = target.strftime("%d %B %Y, %H:%M")
        elif seconds:
            timestamp = target.strftime("%d %B %Y, %H:%M:%S")
        else:
            timestamp = target.strftime("%d %B %Y")

        if isinstance(target, int) or isinstance(target, float):
            target = datetime.datetime.utcfromtimestamp(target)
            target = calendar.timegm(target.timetuple())

        if ago:
            timestamp += f" ({timesince.format(target)})"
        if only_ago:
            timestamp = timesince.format(target)

        return f"{timestamp} (UTC)"
    else:
        unix = int(time.mktime(target.timetuple()))
        timestamp = f"<t:{unix}:{'f' if clock else 'D'}>"
        if ago:
            timestamp += f" (<t:{unix}:R>)"
        if only_ago:
            timestamp = f"<t:{unix}:R>"
        return timestamp

@bot.command()
async def say(ctx, *, arg):
    await ctx.send(arg)

@bot.command()
async def hello(ctx):
    await ctx.send("Приветик! Как делишки?")

@bot.command()
async def megaping(ctx):
    await ctx.send("@everyone!")

@bot.command()
async def cho_delaesh(ctx):
    await ctx.send("Я жду релиза, а ты?")

@bot.command()
async def cool(ctx):
    await ctx.send("Это хорошо! У меня тоже все круто!")

@bot.command()
async def communicate(ctx):
    await ctx.send("Ясно, приятного общение с участниками!")

@bot.command()
async def bye(ctx):
    await ctx.send("Поки, а ты приятный собеседник)")

@bot.command()
async def embed(ctx, *, content: str):
    await ctx.channel.purge(limit=1)
    title, description = content.split("|")
    embed = nextcord.Embed(
        title=title,
        description=description,
        color=nextcord.Color.purple(),
        timestamp=ctx.message.created_at,
    )
    await ctx.send(embed=embed)

@bot.command(usage="[server]")
async def server(ctx):
    emb=nextcord.Embed(title=ctx.guild.name, timestamp=ctx.message.created_at, color=nextcord.Color.purple())
    emb.add_field(name='Участников:', value=ctx.guild.member_count, inline=False)
    emb.add_field(name='Ролей:', value=len(ctx.guild.roles), inline = False)
    emb.add_field(name='Владелец:', value=ctx.guild.owner.mention, inline = False)
    emb.add_field(name='Айди:', value=ctx.guild.id, inline = False)
    emb.add_field(name="server_created_name", value=f"<t:{int(ctx.guild.created_at.timestamp())}:F>, {(nextcord.utils.utcnow()-ctx.guild.created_at).days} days ago", inline=False)
    emb.set_author(name=bot.user.name, icon_url=bot.user.display_avatar)
    emb.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar)
    await ctx.send(embed=emb)

@bot.slash_command(name="server", description="Посмотреть информацию о сервер")
async def server(ctx):
    emb=nextcord.Embed(title=ctx.guild.name,color=nextcord.Color.purple())
    emb.add_field(name='Участников:', value=ctx.guild.member_count, inline=False)
    emb.add_field(name='Ролей:', value=len(ctx.guild.roles), inline = False)
    emb.add_field(name='Владелец:', value=ctx.guild.owner.mention, inline = False)
    emb.add_field(name='Айди:', value=ctx.guild.id, inline = False)
    emb.add_field(name="server_created_name", value=f"<t:{int(ctx.guild.created_at.timestamp())}:F>, {(nextcord.utils.utcnow()-ctx.guild.created_at).days} days ago", inline=False)
    emb.set_author(name=bot.user.name, icon_url=bot.user.display_avatar)
    await ctx.send(embed=emb) 

@bot.command(usage="[пользователь]")
async def user(ctx, *, user: nextcord.Member):
    if not user:
        user = ctx.author

    if user.bot:
        suffix = "боте!"
    else:
        suffix = "пользователе!"
    res = nextcord.Embed(
        title=nextcord.utils.escape_markdown(str(user)),
        description="Информация о " + suffix,
    )
    res.set_author(name=bot.user.name, icon_url=bot.user.display_avatar)
    res.set_thumbnail(url=user.display_avatar)
    res.add_field(name="Айди:", value=user.id, inline=False)
    res.add_field(
        name="Аккаунт создан:",
        value=f"{date(user.created_at, ago=True)}",
        inline=False,
    )
    if ctx.guild:
        if user in ctx.guild.members:
            res.add_field(
                name="Участник присоединился:",
                value=f"{date(user.joined_at, ago=True)}",
                inline=False,
            )
        else:
            res.add_field(
                name="Участник присоединился:",
                value=f"{date(user.joined_at, ago=True)}",
                inline=False,
            )
    await ctx.send(embed=res)

@bot.slash_command(name="user", description="Посмотреть информацию о пользователе")
async def user(ctx, *, user: nextcord.Member):
    if not user:
        user = ctx.author

    if user.bot:
        suffix = "боте!"
    else:
        suffix = "пользователе!"
    res = nextcord.Embed(
        title=nextcord.utils.escape_markdown(str(user)),
        description="Информация о " + suffix,
    )
    res.set_author(name=bot.user.name, icon_url=bot.user.display_avatar)
    res.set_thumbnail(url=user.display_avatar)
    res.add_field(name="Айди:", value=user.id, inline=False)
    res.add_field(
        name="Аккаунт создан:",
        value=f"{date(user.created_at, ago=True)}",
        inline=False,
    )
    if ctx.guild:
        if user in ctx.guild.members:
            res.add_field(
                name="Участник присоединился:",
                value=f"{date(user.joined_at, ago=True)}",
                inline=False,
            )
        else:
            res.add_field(
                name="Участник присоединился:",
                value=f"{date(user.joined_at, ago=True)}",
                inline=False,
            )
    await ctx.send(embed=res)  

@bot.slash_command(name="bite", description="Укусить пользователя")
async def bite (interaction : Interaction, member : nextcord.Member, *, text = None):
    bite = ["https://i.waifu.pics/cnTLq9v.gif", "https://i.waifu.pics/9WRtGbr.gif", "https://i.waifu.pics/UgYmj1t.gif", "https://i.waifu.pics/iErgSVO.gif", "https://i.waifu.pics/W0VmZno.gif", "https://i.waifu.pics/YTKHSD4.gif", "https://i.waifu.pics/PulivJk.gif", "https://i.waifu.pics/bKScj44.gif", "https://i.waifu.pics/asvURcX.gif"]
    if text == None:
        emb1 = nextcord.Embed(title='', description=f'😈 Вы **укусили** {member.mention}')
        emb1.set_image(url=f'{random.choice(bite)}')
        await (interaction.response.send_message(embed=emb1))
    else:
        emb = nextcord.Embed(title='', description=f'😈 Вы **укусили** {member.mention}\n *Комментарий*: {text}')
        emb.set_image(url=f'{random.choice(bite)}')
        await (interaction.response.send_message(embed=emb))

@bot.slash_command(name="pat", description="Погладить пользователя")
async def pat (interaction : Interaction, member : nextcord.Member, *, text = None):
    pat = ["https://i.waifu.pics/g~h0cvT.gif", "https://i.waifu.pics/pmOcanl.gif", "https://i.waifu.pics/0U6HeiX.gif", "https://i.waifu.pics/EE-BZm9.gif", "https://i.waifu.pics/jIPKD0Z.gif", "https://i.waifu.pics/J2EF9YT.gif", "https://i.waifu.pics/MGSjX0_.gif", "https://i.waifu.pics/nsvdMrv.gif", "https://i.waifu.pics/I~znmj2.gif"]
    if text == None:
        emb1 = nextcord.Embed(title='', description=f'🤗 Вы **погладили** {member.mention}',)
        emb1.set_image(url=f'{random.choice(pat)}')
        await (interaction.response.send_message(embed=emb1))
    else:
        emb = nextcord.Embed(title='', description=f'🤗 Вы **погладили** {member.mention}\n *Комментарий*: {text}')
        emb.set_image(url=f'{random.choice(pat)}')
        await (interaction.response.send_message(embed=emb))

@bot.slash_command(name="poke", description="Тыкнуть пользователя")
async def poke (interaction : Interaction, member : nextcord.Member, *, text = None):
    poke = ["https://i.waifu.pics/JlDu4xg.gif", "https://i.waifu.pics/vF1NIJu.gif", "https://i.waifu.pics/beT0l4e.gif", "https://i.waifu.pics/8L~QGTf.gif", "https://i.waifu.pics/Yf8glJM.gif", "https://i.waifu.pics/i2mQiAk.gif", "https://i.waifu.pics/1YxdKac.gif"]
    if text == None:
        emb1 = nextcord.Embed(title='', description=f'👉 Вы **тыкнули** {member.mention}')
        emb1.set_image(url=f'{random.choice(poke)}')
        await (interaction.response.send_message(embed=emb1))
    else:
        emb = nextcord.Embed(title='', description=f'👉 Вы **тыкнули** {member.mention}\n *Комментарий*: {text}')
        emb.set_image(url=f'{random.choice(poke)}')
        await (interaction.response.send_message(embed=emb))

@bot.slash_command(name="kill", description="Убить пользователя")
async def kill (interaction : Interaction, member : nextcord.Member, *, text = None):
    kill = ["https://i.waifu.pics/ETWB-ef.gif", "https://i.waifu.pics/OByL0MA.gif", "https://i.waifu.pics/7Z1tV23.gif", "https://i.waifu.pics/hGFuwrQ.gif", "https://i.waifu.pics/judBJyS.gif", "https://i.waifu.pics/lgsRSai.gif", "https://i.waifu.pics/8uhQSdY.gif", "https://i.waifu.pics/hsAy9-u.gif"]
    if text == None:
        emb1 = nextcord.Embed(title='', description=f'💀 Вы **убили** {member.mention}')
        emb1.set_image(url=f'{random.choice(kill)}')
        await (interaction.response.send_message(embed=emb1))
    else:
        emb = nextcord.Embed(title='', description=f'💀 Вы **убили** {member.mention}\n *Комментарий*: {text}')
        emb.set_image(url=f'{random.choice(kill)}')
        await (interaction.response.send_message(embed=emb))

@bot.slash_command(name="angry", description="Злиться на пользователя")
async def angry (interaction : Interaction, member : nextcord.Member, *, text = None):
    angry = ["https://c.tenor.com/-aieB6Qw8YQAAAAd/anime-angry.gif", "https://c.tenor.com/wtSs_VCHYmEAAAAC/noela-angry.gif", "https://c.tenor.com/jgFVzr3YeJwAAAAC/date-a-live-rage.gif", "https://c.tenor.com/B2G5s1cY7GUAAAAC/anime-angry.gif", "https://c.tenor.com/X3x3Y2mp2W8AAAAC/anime-angry.gif"]
    if text == None:
        emb1 = nextcord.Embed(title='', description=f'😠 Вы **разозлены на** {member.mention}')
        emb1.set_image(url=f'{random.choice(angry)}')
        await (interaction.response.send_message(embed=emb1))
    else:
        emb = nextcord.Embed(title='', description=f'😠 Вы **разозлены на** {member.mention}\n *Комментарий*: {text}')
        emb.set_image(url=f'{random.choice(angry)}')
        await (interaction.response.send_message(embed=emb))

@bot.slash_command(name="lewd", description="Смутиться на пользователя")
async def lewd (interaction : Interaction, member : nextcord.Member, *, text = None):
    lewd = ["https://c.tenor.com/2iEVFFCbPj4AAAAC/momokuri-anime-blush.gif", "https://c.tenor.com/Tk2xYonmrsEAAAAC/anime-blushing.gif", "https://c.tenor.com/bEes0xCurvMAAAAC/anime-blush-dizzy.gif", "https://c.tenor.com/HAWlr1X00Y8AAAAC/anime-love.gif"]
    if text == None:
        emb1 = nextcord.Embed(title='', description=f'😊 Вы **смущены на** {member.mention}')
        emb1.set_image(url=f'{random.choice(lewd)}')
        await (interaction.response.send_message(embed=emb1))
    else:
        emb = nextcord.Embed(title='', description=f'😊 Вы **смущены на** {member.mention}\n *Комментарий*: {text}')
        emb.set_image(url=f'{random.choice(lewd)}')
        await (interaction.response.send_message(embed=emb))

@bot.slash_command(name="kiss", description="Поцеловать пользователя")
async def kiss (interaction : Interaction, member : nextcord.Member, *, text=None):
    kiss = ["https://c.tenor.com/VTvkMN6P648AAAAC/anime-kiss.gif", "https://c.tenor.com/16MBIsjDDYcAAAAC/love-cheek.gif", "https://c.tenor.com/Ge4DoX5aDD0AAAAC/love-kiss.gif", "https://c.tenor.com/JQ9jjb_JTqEAAAAC/anime-kiss.gif", "https://c.tenor.com/I8kWjuAtX-QAAAAC/anime-ano.gif"]
    if text == None:
        emb1 = nextcord.Embed(title='', description=f'❤️ Вы **поцеловали** {member.mention}')
        emb1.set_image(url=f'{random.choice(kiss)}')
        await (interaction.response.send_message(embed=emb1))
    else:
        emb = nextcord.Embed(title='', description=f'❤️ Вы **поцеловали** {member.mention}\n *Комментарий*: {text}')
        emb.set_image(url=f'{random.choice(kiss)}')
        await (interaction.response.send_message(embed=emb))

@bot.slash_command(name="slap", description="Ударить пользователя")
async def slap (interaction : Interaction, member : nextcord.Member, *, text=None):
    slap = ["https://c.tenor.com/1lJTSPaUfKkAAAAd/chika-fujiwara-fwap.gif", "https://c.tenor.com/1-1M4PZpYcMAAAAd/tsuki-tsuki-ga.gif", "https://c.tenor.com/E4Px9kJOQ5wAAAAC/anime-kid.gif", "https://c.tenor.com/iDdGxlZZfGoAAAAC/powerful-head-slap.gif", "https://c.tenor.com/wOCOTBGZJyEAAAAC/chikku-neesan-girl-hit-wall.gif", "https://tenor.com/view/saki-saki-kanojo-mo-kanojo-kmk-saki-anime-gif-22206764"]
    if text == None:
        emb1 = nextcord.Embed(title='', description=f'🖐 Вы **ударили** {member.mention}')
        emb1.set_image(url=f'{random.choice(slap)}')
        await (interaction.response.send_message(embed=emb1))
    else:
        emb = nextcord.Embed(title='', description=f'🖐 Вы **ударили** {member.mention}\n *Комментарий*: {text}')
        emb.set_image(url=f'{random.choice(slap)}')
        await (interaction.response.send_message(embed=emb))

@bot.slash_command(name="hug", description="Обнять пользователя")
async def hug (interaction : Interaction, member : nextcord.Member, *, text=None):
    hug = ["https://c.tenor.com/cFhjNVecNGcAAAAC/anime-hug.gif", "https://c.tenor.com/PuuhAT9tMBYAAAAC/anime-cuddles.gif", "https://c.tenor.com/ixaDEFhZJSsAAAAC/anime-choke.gif", "https://c.tenor.com/qF7mO4nnL0sAAAAC/abra%C3%A7o-hug.gif", "https://c.tenor.com/uIBg3BLATf0AAAAC/hug-darker.gif", "https://c.tenor.com/ncblDAj_2FwAAAAC/abrazo-hug.gif", "https://c.tenor.com/QCQV57yhBMsAAAAd/comforting-hug.gif"]
    if text ==None:
        emb1 = nextcord.Embed(title='', description=f'👐 Вы **обняли** {member.mention}')
        emb1.set_image(url=f'{random.choice(hug)}')
        await (interaction.response.send_message(embed=emb1))
    else:
        emb = nextcord.Embed(title='', description=f'👐 Вы **обнялаи** {member.mention}\n *Комментарий*: {text}')
        emb.set_image(url=f'{random.choice(hug)}')
        await (interaction.response.send_message(embed=emb))

@bot.slash_command(name="feed", description="Покормить пользователя")
async def feed (interaction : Interaction, member : nextcord.Member, *, text=None):
    feed = ["https://i.waifu.pics/g6ISmbU.gif", "https://i.waifu.pics/on3fsaG.gif", "https://i.waifu.pics/9cuZ2_c.gif", "https://i.waifu.pics/_Xhrs1u.gif", "https://i.waifu.pics/GfZNQ63.gif", "https://i.waifu.pics/v-zBxL0.gif", "https://i.waifu.pics/4Kqzf3o.gif", "https://i.waifu.pics/FJyxFzB.gif", "https://i.waifu.pics/-OvwPE6.gif"]
    if text == None:
        emb1 = nextcord.Embed(title='', description=f'🍕 Вы **покормили** {member.mention}')
        emb1.set_image(url=f'{random.choice(feed)}')
        await (interaction.response.send_message(embed=emb1))
    else:
        emb = nextcord.Embed(title='', description=f'🍕 Вы **покормили** {member.mention}\n *Комментарий*: {text}')
        emb.set_image(url=f'{random.choice(feed)}')
        await (interaction.response.send_message(embed=emb))

@bot.slash_command(name="smile", description="Улыбнуться перед пользователем")
async def smile (interaction : Interaction, member : nextcord.Member, *, text = None):
    smile = ["https://i.waifu.pics/7lhMNMV.gif", "https://i.waifu.pics/u8drjx7.gif", "https://i.waifu.pics/4RMgMWL.gif", "https://i.waifu.pics/tvSCzkl.gif", "https://i.waifu.pics/MGiBjN-.gif", "https://i.waifu.pics/Uvqo6Mz.gif", "https://i.waifu.pics/mhLpKn5.gif", "https://i.waifu.pics/jGcj2CQ.gif", "https://i.waifu.pics/73ri7VG.gif", "https://i.waifu.pics/xyuju7Q.gif"]
    if text == None:
        emb1 = nextcord.Embed(title='', description=f'🙂 Вы **улыбнулись перед** {member.mention}')
        emb1.set_image(url=f'{random.choice(smile)}')
        await (interaction.response.send_message(embed=emb1))
    else:
        emb = nextcord.Embed(title='', description=f'🙂 Вы **улыбнулись** перед {member.mention}\n *Комментарий*: {text}')
        emb.set_image(url=f'{random.choice(smile)}')
        await (interaction.response.send_message(embed=emb))

@bot.slash_command(name="lick", description="Облизать пользователя")
async def lick (interaction : Interaction, member : nextcord.Member, *, text = None):
    lick = ["https://c.tenor.com/4U2-K7XUIJUAAAAC/pain-ellenoar.gif", "https://c.tenor.com/uw6-q_y4xKsAAAAd/%D0%B0%D0%BD%D0%B8%D0%BC%D0%B5-darling-in-the-franxx.gif", "https://i.waifu.pics/iL8UVFd.gif", "https://i.waifu.pics/hV9cyEJ.gif", "https://c.tenor.com/0LMxPQdFBKAAAAAC/nekopara-kiss.gif", "https://i.waifu.pics/LyVaHfl.gif", "https://i.waifu.pics/JxQolYt.gif", "https://i.waifu.pics/at~DQwu.gif"]
    if text == None:
        emb1 = nextcord.Embed(title='', description=f'😛 Вы **облизали** {member.mention}')
        emb1.set_image(url=f'{random.choice(lick)}')
        await (interaction.response.send_message(embed=emb1))
    else:
        emb = nextcord.Embed(title='', description=f'😛 Вы **облизали** {member.mention}\n *Комментарий*: {text}')
        emb.set_image(url=f'{random.choice(lick)}')
        await (interaction.response.send_message(embed=emb))

@bot.slash_command(name="wave", description="Приветствовать пользователя")
async def wave (interaction : Interaction, member : nextcord.Member, *, text = None):
    wave = ["https://i.waifu.pics/wyVFEi7.gif", "https://i.waifu.pics/SNR4nf5.gif", "https://i.waifu.pics/Jvi3~TN.gif", "https://i.waifu.pics/iC7niFP.gif", "https://i.waifu.pics/s3G5xJ0.gif", "https://i.waifu.pics/RtR0LFI.gif", "https://i.waifu.pics/KEPtqkH.gif", "https://i.waifu.pics/T0gfAdU.gif", "https://i.waifu.pics/8npsaf-.gif", "https://i.waifu.pics/l3_ObDa.gif", "https://i.waifu.pics/546M14t.gif"]
    if text == None:
        emb1 = nextcord.Embed(title='', description=f'👋 Вы **приветствуете** {member.mention}')
        emb1.set_image(url=f'{random.choice(wave)}')
        await (interaction.response.send_message(embed=emb1))
    else:
        emb = nextcord.Embed(title='', description=f'👋 Вы **приветствуете** {member.mention}\n *Комментарий*: {text}')
        emb.set_image(url=f'{random.choice(wave)}')
        await (interaction.response.send_message(embed=emb))

@bot.slash_command(name="say", description="Написать от лица бота")
async def say(ctx, *, arg):
    await ctx.send(arg)

@bot.slash_command(name="ping", description="Посмотреть пинг")
async def ping(ctx):
    await ctx.send(f"🏓 My ping is {round(bot.latency * 1000)}ms")

@bot.slash_command(name="hello", description="Сказать боту Привет")
async def hello(ctx):
    await ctx.send(f"Приветик! Как дела?")

@bot.slash_command(name="cool", description="Ответить на ( привет )")
async def cool(ctx):
    await ctx.send(f"Это хорошо! У меня тоже все круто!")

@bot.slash_command(name="cho_delaesh", description="Спросить, что делает бот?")
async def cho_delaesh(ctx):
    await ctx.send(f"Я жду релиза, а ты?)")

@bot.slash_command(name="communicate", description="Ответ от бота на ( Чо делаешь? )")
async def communicate(ctx):
    await ctx.send(f"Ясно, приятного общение с участниками!")

@bot.slash_command(name="bye", description="По прощяться с Аксей!")
async def bye(ctx):
    await ctx.send(f"Поки, а ты приятный собеседник)")

@bot.slash_command(name="prefix", description="Посмотреть префикс бота!")
async def prefix(ctx):
    await ctx.send(f"Мой префикс `?` <3")

@bot.event
async def on_ready():
    print("BOT connected")
    await bot.change_presence(
        status=nextcord.Status.online,
        activity=nextcord.Streaming(
            name="BetaTest | Beta 1.0.0", url="https://www.twitch.tv/twitch"
        ),
    )

start_time = utcnow()

bot.run('')