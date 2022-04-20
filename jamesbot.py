from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import azure.cognitiveservices.speech as speechsdk
import os
import discord
import random
import time
import threading
import asyncio
import mutagen
from mutagen.mp3 import MP3
from discord.ext import commands, tasks
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
from datetime import datetime


load_dotenv()
intent = discord.Intents().default()
intent.voice_states = True
intent.members = True
TOKEN = os.getenv('DISCORD_TOKEN')
NEWSALERT = os.getenv('NEWS_ALERT')
bot=commands.Bot(command_prefix='$', intents=intent)
speech_key = os.getenv('SPEECH_TOKEN')
service_region = os.getenv('SERVICE_REGION')
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
sounddir = "C:/Users/connf/Downloads/"
root = ET.parse("C:/Users/connf/Downloads/jamesbotsounds.spl")
sounds = []
guildslist = []
random.seed()
bslistlist = []
i = 0
b = 0
bs = 0
ctxlist = []
for s in root.findall('Sound'):
    sounds.append(sounddir + s.get('url'))


def get_random_sound():
    size = len(sounds)
    return sounds[random.randint(0, size-1)]

@bot.event          
async def on_ready():
    global guildslist
    print(f'{bot.user} has connected to Discord!')
    guildslist = await bot.fetch_guilds().flatten()
    bot.loop.create_task(time_checker())
    
@bot.event
async def on_connect():
    i = 0
        
@bot.command()
async def j(ctx):
    global i, ctxlist, sounds
    i += 1
    ctxlist.append(ctx)
    voice_channel = ctx.author.voice.channel
    channel = None
    isplaying = False
    if voice_channel != None and not isplaying:
        channel = voice_channel.name
        vc = await voice_channel.connect()
        while i > 0:
            s = get_random_sound()
            vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg-N-101953-g4e64c8fa29-win64-gpl-shared/bin/ffmpeg.exe", source=s))
            # Sleep while audio is playing.
            while vc.is_playing():
                if not isplaying:
                    isplaying = True
                time.sleep(.1)
            if len(ctxlist) > 0:
                await ctxlist.pop().message.delete()
            i -= 1
        await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")
        
@bot.command()
async def news(ctx):
    global i, ctxlist, sounds
    print(NEWSALERT)
    i += 1
    ctxlist.append(ctx)
    voice_channel = ctx.author.voice.channel
    channel = None
    isplaying = False
    if voice_channel != None and not isplaying:
        channel = voice_channel.name
        vc = await voice_channel.connect()
        s = get_random_sound()
        vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg-N-101953-g4e64c8fa29-win64-gpl-shared/bin/ffmpeg.exe", source=NEWSALERT, options="-filter:a \"volume=0.1\""))
        # Sleep while audio is playing.
        while vc.is_playing():
            if not isplaying:
                isplaying = True
            time.sleep(.1)
        vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg-N-101953-g4e64c8fa29-win64-gpl-shared/bin/ffmpeg.exe", source=s))
        # Sleep while audio is playing.
        while vc.is_playing():
            if not isplaying:
                isplaying = True
            time.sleep(.1)
        if len(ctxlist) > 0:
            await ctxlist.pop().message.delete()
        await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")
@bot.command()
async def clear(ctx):
    global b, ctxlist
    b = 0
    ctxlist.append(ctx)
    if len(ctxlist) > 0:
        await ctxlist.pop().message.delete()
                    
@bot.command()
async def blend(ctx, *args):
    global b, ctxlist
    b += 1
    if args.__len__() > 0:
        if args[0].isnumeric():
            repeatNum = int(args[0])
            if repeatNum >= 0:
                b += repeatNum%30
    ctxlist.append(ctx)
    voice_channel = ctx.author.voice.channel
    channel = None
    isplaying = False
    channel = voice_channel.name
    if voice_channel != None:
        vc = await voice_channel.connect()
        while b > 0:
            n = random.randint(2, 7)
            while n > 0:
                print("starting new loop")
                print(n)
                s = get_random_sound()
                tracklength = int(MP3(s).info.length)
                while tracklength == 0:     
                    s = get_random_sound()
                    tracklength = int(MP3(s).info.length)
                #print(tracklength)
                timestamp = random.randint(0, tracklength)
                #print(timestamp)
                if tracklength - timestamp <= 1:
                    timestamp = 0
                duration = 0
                while duration == 0 and duration <= 8:  
                    rando = random.randint(timestamp, tracklength) - timestamp
                    if tracklength < 2:
                        if rando <= 2:
                            duration = rando
                    else:
                        if rando >= 2 and rando <= 10:
                            duration = rando
                vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg-N-101953-g4e64c8fa29-win64-gpl-shared/bin/ffmpeg.exe", source=s, options=f"-vn -ss {timestamp} -t {duration}"))
                # Sleep while audio is playing.
                while vc.is_playing():
                    if not isplaying:
                        isplaying = True
                    time.sleep(.1)
                print("finished playing")
                print(s)
                n -= 1
            b -= 1          
        print("reached msg delete")
        if len(ctxlist) > 0:
            await ctxlist.pop().message.delete() 
        print("reached disconenct")
        await vc.disconnect()
        
        

@bot.command()
async def blend_s(ctx, *args):
    global bs, ctxlist, bslistlist
    bs += 1
    ctxlist.append(ctx)
    voice_channel = ctx.author.voice.channel
    channel = None
    isplaying = False
    if voice_channel != None: 
        soundnames = []
        soundtimestamps = []
        j = 0
        k = 0
        for n in args:
            if n.find(":") == -1:
                soundnames.append(sounddir + n + ".mp3")
                print("Added " + sounddir + n + " .mp3")
                soundtimestamps.append(None)
                j += 1
            else:
                while k < len(soundnames)-1:
                    k += 1
                t = n.split(":")
                soundtimestamps[k] = t
        bslistlist.append(soundnames)
        bslistlist.append(soundtimestamps)
        if not isplaying:
            channel = voice_channel.name
            vc = await voice_channel.connect()
            while bs > 0:
                sn = bslistlist.pop(0)
                sts = bslistlist.pop(0)
                for s in sn:
                    temp = sts.pop(0)
                    if temp == None:
                        vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg-N-101953-g4e64c8fa29-win64-gpl-shared/bin/ffmpeg.exe", source=s))
                        while vc.is_playing():
                            if not isplaying:
                                isplaying = True
                            time.sleep(.1)
                    else:
                        timestamp = int(temp.pop(0))
                        duration = int(temp.pop(0)) - timestamp
                        if duration > 0 and timestamp >= 0 and timestamp < MP3(s).info.length:
                            duration = MP3(s).info.length - timestamp
                            vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg-N-101953-g4e64c8fa29-win64-gpl-shared/bin/ffmpeg.exe", source=s, options=f"-vn -ss {timestamp} -t {duration}"))  
                            while vc.is_playing():
                                if not isplaying:
                                    isplaying = True
                                time.sleep(.1)
                print("finished playing")
                print(s)
                bs -= 1
            if len(ctxlist) > 0:
                await ctxlist.pop().message.delete()
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")
            
            
@bot.command()        
async def sounds_info(ctx):
    m = "==========SOUND NAME - DURATION (SECONDS)==========\n"
    for i in sounds:
        duration = MP3(i).info.length
        while i.find("/") != -1:
            i = (i[i.find("/")+1:])
        i = i[:i.find(".")]
        m += f'"{i}" - {duration:4.3}s\n' 
    print(len(m))
    await ctx.author.send(m)
    
@bot.command()
async def jhelp(ctx):
    await ctx.author.send("------Welcome to JamesBot: the Magic James Ball------\nThe currently loaded list of commands is as follows:\n$j - Play a random clip in your voice channel.\n$blend - Play a mashup of bits from several different clips.\n$news - Play a news announcement in your current voice channel.\n$blend_s - Queue a specific selection of clips or partial clips, used as: $blend_s \"clip1\" 0:2 \"clip2\" \"clip3\" 3:4.\n$sounds_info - Request a dm of the list of sound files currently loaded (Warning: may be long).")

async def hourly_news_report():
    global guildslist
    for g in guildslist:
        if g.name == "<Darkshire Trap House>":
            d = bot.get_guild(g.id)
            for c in d.voice_channels:
                if len(c.members) > 0 and c.name != "AFK" and c.name != "Porky's Prison":
                    channel = c.name
                    vc = await c.connect()
                    s = get_random_sound()
                    vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg-N-101953-g4e64c8fa29-win64-gpl-shared/bin/ffmpeg.exe", source=NEWSALERT, options="-filter:a \"volume=0.1\""))
                    # Sleep while audio is playing.
                    while vc.is_playing():
                        time.sleep(.1)
                    vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg-N-101953-g4e64c8fa29-win64-gpl-shared/bin/ffmpeg.exe", source=s))
                    # Sleep while audio is playing.
                    while vc.is_playing():
                        time.sleep(.1)
                    await vc.disconnect()
    
async def time_checker():
    while True:
        m = datetime.now().strftime("%M")
        s = datetime.now().strftime("%S")
        if (m == "00") and (s == "00"):
            await hourly_news_report()
        await asyncio.sleep(1)
            
bot.run(TOKEN)