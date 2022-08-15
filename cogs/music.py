import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
import requests
from bs4 import BeautifulSoup
import asyncio
import time
import os


class music_bot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.start = 0
        self.duration = 0
        self.pause_flag = 0
        self.music_index = 0
        self.music_length = 0
        self.music_name_local = './music_name.txt'
        self.music_url_local = './music_url.txt'
        self.path = '../music/'
        self.music_name_list=list()
        self.music_url_list=list()
        self.read_list()
       
    def read_list(self):
        with open(self.music_name_local,'r',encoding="utf-8") as f:
            line = f.readline()    
            while line:  
                line = line.split('\n')
                self.music_name_list.append(line[0])
                line = f.readline()
        f.close()
        with open(self.music_url_local,'r',encoding="utf-8") as f:
            line = f.readline()    
            while line:  
                line = line.split('\n')
                self.music_url_list.append(line[0])
                line = f.readline()
        f.close()
        return 
          
    def save_list(self):
        with open(self.music_name_local,'w',encoding="utf-8") as f:
            for name in self.music_name_list:
                print(name,file=f)
        f.close()
        with open(self.music_url_local,'w',encoding="utf-8") as f:
            for url in self.music_url_list:
                print(url,file=f)
        f.close()
             
    async def delete_list(self,ctx,target):
        if(int(target) < 1 or int(target) > len(self.music_name_list)):
            await ctx.send('請輸入正確的數字...')
            return 

        del self.music_name_list[int(target)-1]
        del self.music_url_list[int(target)-1]
        self.save_list()
        if(int(target)-1<=self.music_index):
            self.music_index = self.music_index - 1
        await ctx.send('已刪除第'+str(target)+'條歌曲')  
    
    @commands.command()
    async def move(self,ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

    @commands.command()
    async def s(self,ctx,keyword):
        response = requests.get('https://www.youtube.com/results?search_query='+str(keyword)+'&sp=CAASAhAB')
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all('script')
        number = 35
        index = 0
        for result in results:
            index = index + 1 
            if(index==number):
                string = result.getText()
        embed=discord.Embed()
        a=b=c=i=0
        for i in range(3):
            a=string.find("\"title\":",int(a+1))
            b=string.find(",",int(a+1))
            c=string.find("videoId",int(b+1))
            embed.add_field(name=string[a+26:b-2], value='https://www.youtube.com/watch?v='+string[c+10:c+21], inline=False)
            
        await ctx.channel.send(embed=embed) 
    
    def next_music(self,ctx):  
        voice = get(self.bot.voice_clients, guild=ctx.guild) 
        self.music_index = self.music_index + 1
        if(self.music_index  == len(self.music_url_list)):
            self.music_index = 0 
        YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'outtmpl': self.path+str(self.music_url_list[self.music_index][32:43])+'.opus',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredquality': '320',
            }]   
        }
        url = self.music_url_list[self.music_index]
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        self.music_length = '0' + str(info['duration_string'])   
        if(os.path.isfile(self.path+str(self.music_url_list[self.music_index][32:43])+'.opus')):
            audio = discord.FFmpegPCMAudio(self.path+str(self.music_url_list[self.music_index][32:43])+'.opus')
            print('從local端播放音樂:'+str(self.music_name_list[self.music_index]))                      
            self.duration = 0
            self.start = time.time()
            voice.play(audio, after= lambda e:self.next_music(ctx))
        else:          
            url = self.music_url_list[self.music_index]
            with YoutubeDL(YDL_OPTIONS) as ydl:
                ydl.download([url])        
            print('下載音樂：'+str(self.music_name_list[self.music_index]))
            audio = discord.FFmpegPCMAudio(self.path+str(self.music_url_list[self.music_index][32:43])+'.opus')
            self.duration = 0
            self.start = time.time()
            voice.play(audio, after= lambda e:self.next_music(ctx))
            
            
    @commands.command()
    async def play(self,ctx):  
        print('開始播放音樂')   
        voice = get(self.bot.voice_clients, guild=ctx.guild) 
        YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'outtmpl': self.path+str(self.music_url_list[self.music_index][32:43])+'.opus',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredquality': '320',
            }]   
        }
        url = self.music_url_list[self.music_index]
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        self.music_length = '0' + str(info['duration_string'])
        if not voice.is_playing():
            if(os.path.isfile(self.path+str(self.music_url_list[self.music_index][32:43])+'.opus')):
                print('從local端播放音樂:'+str(self.music_name_list[self.music_index]))
                audio = discord.FFmpegPCMAudio(self.path+str(self.music_url_list[self.music_index][32:43])+'.opus')                    
                self.duration = 0
                self.start = time.time()   
                voice.play(audio, after= lambda e:self.next_music(ctx))
            else:
                url = self.music_url_list[self.music_index]
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    ydl.download([url])           
                print('下載音樂：'+str(self.music_name_list[self.music_index]))
                audio = discord.FFmpegPCMAudio(self.path+str(self.music_url_list[self.music_index][32:43])+'.opus')
                self.duration = 0
                self.start = time.time()
                voice.play(audio, after= lambda e:self.next_music(ctx)) 

    @commands.command()
    async def resume(self,ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            self.pause_flag = 0
            self.start = time.time()
            voice.resume()
            
    @commands.command()
    async def pause(self,ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            self.pause_flag = 1
            self.duration += time.time()-self.start
            voice.pause()
           
    @commands.command()
    async def skip(self,ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
    
    @commands.command()
    async def mskip(self,ctx,value):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            self.music_index = int(value)-2
            voice.stop()

    @commands.command()
    async def show(self,ctx):
        number = 1
        output_str = ''
        for name in self.music_name_list :
            if(name[0]!='\n'):
                tmp = str(number)+'. '+ name + '\n' 
                output_str += tmp
                number = number + 1   
        now = 0
        while(len(output_str)>1900):
            now = output_str.find('\n',int(1900))
            await ctx.send(output_str[0:now])
            output_str = output_str[now:-1]
        await ctx.send(output_str)
       
            

    @commands.command()  
    async def add(self,ctx,url):
        idx = str(url).find('&',0)
        if(idx==-1):
            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'nocheckcertificate': True,}
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)   
            self.music_name_list.append(info['title'])
            with open(self.music_name_local, 'a',encoding="utf-8") as f:
                print(info['title'],file=f)
            f.close()
            with open(self.music_url_local, 'a',encoding="utf-8") as f:
                print(url,file=f)
            f.close()
            self.music_url_list.append(url)
            await ctx.channel.send('新增歌曲:'+str(info['title'])+'成功')
        else:
            await ctx.send('請確認網址正確(不可包含歌單)！')     
    @commands.command()  
    async def remove(self,ctx,number):
        await self.delete_list(ctx,number)  

    @commands.command()          
    async def help_music(self,ctx):
        embed=discord.Embed(title="指令列表", description="音樂機器人所有指令", color=0x000000)
        embed.add_field(name="[play", value="開始播放", inline=True)
        embed.add_field(name="[pause", value="暫停播放", inline=True)
        embed.add_field(name="[resume", value="繼續播放", inline=True)
        embed.add_field(name="[skip", value="跳過此首歌曲進入下一首", inline=True)
        embed.add_field(name="[s", value="查詢歌曲(search後請輸入關鍵字)", inline=False)
        embed.add_field(name="[show", value="顯示目前音樂列表", inline=False)
        embed.add_field(name="[add", value="新增歌曲(add後請輸入url)", inline=True)  
        embed.add_field(name="[remove", value="移除歌曲(remove後請輸入要刪除的歌曲編號) Ex. [remove 3", inline=False)
        embed.add_field(name="[np", value ="目前播放狀態",inline=False)
        await ctx.channel.send(embed=embed)        
    
    @commands.command()      
    async def np(self,ctx):
        image_url = 'https://i1.ytimg.com/vi/'+str(self.music_url_list[self.music_index][32:43])+'/maxresdefault.jpg' 
        if(self.pause_flag == 0):
            self.duration += time.time()-self.start
        self.start = time.time()
        title = '目前播放'
        m,s=divmod(self.duration,60)
        name = str(self.music_name_list[self.music_index])+' ( '+str(self.music_index+1)+' / '+str(len(self.music_url_list))+' )'
        value = "0"+str(round(m))+":"
        if(round(s)<10):
            value += "0"+str(round(s))
        else:
            value += str(round(s))
        value += ' / '+str(self.music_length)
        embed=discord.Embed(title=title, color=0x000000)
        embed.add_field(name=name,value=value)
        embed.set_thumbnail(url=image_url)
        await ctx.channel.send(embed=embed)
          
def setup(bot):
    bot.add_cog(music_bot(bot))
    
