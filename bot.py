import discord
from discord.ext import commands
import os
from discord.utils import get
import asyncio
import os

num = 0
intents = discord.Intents.default()
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='[',intents=intents)
bot.load_extension("cogs.music")
bot.load_extension("cogs.member")

music_channel =  #音樂機器人進入頻道
guild_id =  #伺服器ID

@bot.event  # check if bot is ready
async def on_ready():
    global num
    print('Bot is online:'+str(bot.users[0].name))
    print('Discord Edition:'+discord.__version__)
    
    #Enter Music Server
    guild = bot.get_guild(guild_id)
    channel = bot.get_channel(music_channel)
   
    voice = get(bot.voice_clients, guild=guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    num = guild.member_count
    channel = bot.get_channel() 
    await channel.edit(name='目前人數：'+str(num))

@bot.event
async def on_member_join(member):
    global num
    num = num + 1
    channel = bot.get_channel() 
    await channel.edit(name='目前人數：'+str(num))

@bot.event   
async def on_member_remove(member):
    global num
    num = num - 1
    channel = bot.get_channel() 
    await channel.edit(name='目前人數：'+str(num))


@bot.command()
async def reload(ctx,extension):
    bot.reload_extension('cogs.'+str(extension))
    await ctx.send('Reload '+str(extension)+' successful')

@bot.command()
async def load(ctx,extension):
    bot.load_extension('cogs.'+str(extension))
    await ctx.send('Load '+str(extension)+' successful')

if __name__ == '__main__':
    bot.run('')