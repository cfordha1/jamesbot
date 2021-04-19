from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import azure.cognitiveservices.speech as speechsdk
import os
import discord
import random
import time
from discord.ext import commands
from dotenv import load_dotenv
import xml.etree.ElementTree as ET


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot=commands.Bot(command_prefix='$')
speech_key = os.getenv('SPEECH_TOKEN')
service_region = os.getenv('SERVICE_REGION')
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
sounddir = "C:/Users/connf/Downloads/"
root = ET.parse("C:/Users/connf/Downloads/jamesbotsounds.spl")
sounds = []
random.seed()
i = 0
ctxlist = []
for s in root.findall('Sound'):
    sounds.append(sounddir + s.get('url'))


def get_random_sound():
    size = len(sounds)
    return sounds[random.randint(0, size-1)]

@bot.event          
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    
@bot.event
async def on_connect():
    i = 0
        
@bot.command()
async def j(ctx):
    global i, ctxlist
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
            await ctxlist.pop().message.delete()
            i -= 1
        await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")            
    
bot.run(TOKEN)