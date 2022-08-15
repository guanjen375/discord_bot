import discord
from discord.ext import commands
import asyncio
import random
import numpy as np 
import math
import os
import requests

class member(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot     
        self.work_list = list()
        self.daily_list = list()        
        
        self.point = dict()
        self.gem = dict()
        self.gash_list = list()
                
        self.point_local = './member.txt'
        self.gem_local = './gem.txt'
        self.gash_local = './pic/'
        
        self.read_point()
        self.read_gem()
        self.read_gash()
              
        self.guess = 0
        self.g_21 = 0
        self.camel = 0
            
        camel_str = '1.每次玩家可選擇擲骰(骰子點數3/2/1/0/-1)或向前移動一步\n'
        camel_str += '2.BOT每次擲骰(骰子點數3/2/1/0)，先到10者獲勝\n'
        camel_str += '3.兩人位置重疊後到者先骰(骰到0除外)\n'
        camel_str += '4.玩家最多一輪操作2次'
        embed = discord.Embed(title = '規則說明',description=camel_str)
        self.camel_des = embed
        
        g_21_str = '1.玩家點數必須等於或低於21點，超過21點稱為爆牌\n'
        g_21_str += '2.A可記為1點或11點，2點至10點的牌以牌面的點數計算，J、Q、K 每張為10點\n'
        g_21_str += '3.每位玩家的目的是要取得最接近21點數的牌來擊敗BOT，BOT為隨機16-24點'
        embed = discord.Embed(title = '規則說明',description=g_21_str)
        self.g_21_des = embed
        
        guess_str = '1.玩家必須在6次之內猜出號碼(號碼為1-100)\n'
        guess_str += '2.每次猜出數字後系統會給出新的範圍'       
        embed = discord.Embed(title = '規則說明',description=guess_str)
        self.guess_des = embed

    def save_point(self):
        with open(self.point_local,'w',encoding='UTF-8') as f:
            for name in self.point:
                print(str(self.point[name])+' '+str(name),file = f)
            f.close()
       
    def save_gem(self):
        with open(self.gem_local,'w',encoding='UTF-8') as f:
            for name in self.gem:
                print(str(self.gem[name])+' '+str(name),file = f)
            f.close()
      
    def read_point(self):
        with open(self.point_local,'r',encoding='UTF-8') as f:
            line = f.readline()
            while line:  
                line = line.split(' ')
                line1 = line[1].split('\n')
                self.point[str(line1[0])] = int(line[0])
                line = f.readline()
            f.close()
    
    def read_gem(self):
        with open(self.gem_local,'r',encoding='UTF-8') as f:
            line = f.readline()
            while line:  
                line = line.split(' ')
                line1 = line[1].split('\n')
                self.gem[str(line1[0])] = int(line[0])
                line = f.readline()
            f.close()
    def read_gash(self):
        for filename in os.listdir(self.gash_local):
            self.gash_list.append('./pic/'+str(filename))
            print('讀取圖片：'+'pic/'+str(filename)) 
           

    def search_work(self,key):
        for i in range(len(self.work_list)):
            if(self.work_list[i] == key):
                return True
        return False
    
    def search_daily(self,key):
        for i in range(len(self.daily_list)):
            if(self.daily_list[i] == key):
                return True
        return False   
    
    @commands.command()
    async def daily(self,ctx):
        result = self.search_daily(ctx.author)
        if(result == True):
            await ctx.send('🎲'+str(ctx.author)+'，您12小時內已簽到，請稍後再試')
        else:
            await ctx.send('🎲'+str(ctx.author)+'，您已完成簽到，請領取5顆寶石(下次簽到可在12小時後再次簽到)')
            await ctx.send('🎲寶石用途：每顆可增加0.01妞妞獲勝倍率，取得方法：[work(3-6顆)/[guess/[g_21/[camel(3顆)')
            self.daily_list.append(ctx.author)
            self.gem[ctx.author.name] = int(self.gem[ctx.author.name])+5
            self.save_gem()
            await asyncio.sleep(43200)
            self.daily_list.remove(ctx.author)
            await ctx.send('🎲簽到冷卻已結束，'+str(ctx.author.mention))
    
    @commands.command()
    async def work(self,ctx):
        result = self.search_work(ctx.author)
        if(result == True):
            await ctx.send('🎲'+str(ctx.author.mention)+'你目前正在工作，一小時後才能再次工作')
        else:
            await ctx.send('🎲'+str(ctx.author.mention)+'您正在工作中，一小時後領取3-6顆寶石')
            self.work_list.append(ctx.author)
            await asyncio.sleep(3600)
            self.work_list.remove(ctx.author)
            value = random.randint(3,6)
            await ctx.send('🎲'+str(ctx.author.mention)+'工作完成，已領取'+str(value)+'顆寶石')          
            self.gem[ctx.author.name] = int(self.gem[ctx.author.name])+value
            self.save_gem()
     

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,data):
        url = data.emoji.url
        name = data.emoji.name
        r = requests.get(url)
        with open('./pic/'+name+'.jpeg','wb+') as f:
            f.write(r.content)
        self.gash_list.append('./pic/'+str(name)+'.jpeg')
        print('新增貼圖：'+'./pic/'+str(name)+'.jpeg')
        f.close()
       
    @commands.command()
    async def gash(self,ctx):
        if(len(self.gash_list) == 0):
            await ctx.send('🎲轉蛋機內無物品，請設定')
            return 
        result = random.randint(0,len(self.gash_list)-1)
        embed = discord.Embed(title='恭喜'+str(ctx.author.name)+'獲得了')     
        pic = discord.File(self.gash_list[result],filename='image.png')
        embed.set_image(url='attachment://image.png')
        await ctx.send(file=pic,embed=embed)
    
    @commands.command()
    async def register(self,ctx):
        for name in self.point:
            if(name == ctx.author.name):
                await ctx.send('🎲此帳號已註冊，請勿重複註冊！')
                return 
        self.point[ctx.author.name] = int(1000)
        self.gem[ctx.author.name] = int(0)
        await ctx.send('🎲'+str(ctx.author.name)+'註冊成功')
        self.save_gem()
        self.save_point()
    
    @commands.command()
    async def show_gem(self,ctx):
        await ctx.send('目前寶石數量：'+str(self.gem[ctx.author.name]))  
    
    @commands.command()
    async def show_rank(self,ctx):
        self.save_point()
        self.point = dict(sorted(self.point.items(), key=lambda item:item[1],reverse=True))
        embed=discord.Embed(title="財富排行榜")
        i = 1
        for name in self.point:
            output_str = ''
            if int(self.point[name])>0:
                output_str+='('+str(round(np.log2(int(self.point[name])),3))+')'
            embed.add_field(name=str(i)+'.'+str(name)+output_str, value='$'+str(self.point[name]), inline=False)
            i=i+1
        await ctx.send(embed=embed)
  
    @commands.command()
    async def camel(self,ctx):
        if(self.camel == 1):
            await ctx.send('🎲已經有人正在遊玩，請稍後再試')
            return  
        self.camel = 1
        await ctx.send(embed=self.camel_des)   
        move = 0
        a=b=0
        await ctx.send('🎲目前位置 :['+str(a)+' '+str(b)+']，請選擇要擲骰或移動一步？(Y=擲骰/N=移動一步)')
        while(a<10 and b<10):           
            reply = await self.bot.wait_for('message')    
            if(reply.author.name == ctx.author.name and reply.content=='Y' and move < 2):
                move = move + 1
                val = random.randint(-1,3)
                await ctx.send('🎲您骰出了'+str(val))
                a = a + val
                if(a == b and val!=0 and move < 2):
                    await ctx.send('🎲目前位置 :['+str(a)+' '+str(b)+']，請選擇要擲骰或移動一步？(Y=擲骰/N=移動一步)')
                else:
                    move = 0
                    val = random.randint(0,3)
                    await ctx.send('🎲目前位置 :['+str(a)+' '+str(b)+']\n🎲輪到BOT的回合了\n🎲BOT骰出了'+str(val)+'\n')
                    b = b + val
                    if(a==b and val!=0):
                        val = random.randint(0,3)
                        await ctx.send('🎲目前位置 :['+str(a)+' '+str(b)+']\n🎲輪到BOT的回合了\n🎲BOT骰出了'+str(val)+'\n') 
                        b = b + val
                    await ctx.send('🎲目前位置 :['+str(a)+' '+str(b)+']，請選擇要擲骰或移動一步？(Y=擲骰/N=移動一步)')
            if(reply.author.name == ctx.author.name and reply.content=='N' and move < 2):
                move = move + 1
                a = a + 1
                if(a == b and move < 2):
                    await ctx.send('🎲目前位置 :['+str(a)+' '+str(b)+']，請選擇要擲骰或移動一步？(Y=擲骰/N=移動一步)')
                else:   
                    move = 0
                    val = random.randint(0,3)
                    await ctx.send('🎲目前位置 :['+str(a)+' '+str(b)+']\n🎲輪到BOT的回合了\n🎲BOT骰出了'+str(val)+'\n')
                    b = b + val
                    if(a==b and val!=0):
                        val = random.randint(0,3)
                        await ctx.send('🎲目前位置 :['+str(a)+' '+str(b)+']\n🎲輪到BOT的回合了\n🎲BOT骰出了'+str(val)+'\n') 
                        b = b + val
                    await ctx.send('🎲目前位置 :['+str(a)+' '+str(b)+']，請選擇要擲骰或移動一步？(Y=擲骰/N=移動一步)')
                    
        if(a>=10):
            output_str = '🎲恭喜'+str(ctx.author.name)+'得到了3顆寶石' 
            self.gem[ctx.author.name] = int(self.gem[ctx.author.name])+3
        else:
            output_str = '🎲請再接再厲，'+str(ctx.author.name) 
        self.camel = 0
        self.save_gem()        
        await ctx.send(output_str)

    @commands.command()    
    async def guess(self,ctx):
        if(self.guess == 1):
            await ctx.send('🎲已經有人正在遊玩，請稍後再試')
            return    
        self.guess = 1
        await ctx.send(embed=self.guess_des)          
        answer = random.randint(1,100)
        reply = -1
        number = 0
        low = 1
        high = 100
        while(reply!=answer and number < 6):
            reply = await self.bot.wait_for('message')
            if (reply.content.isdigit() and reply.author.name == ctx.author.name):
                if((int)(reply.content)==answer):                  
                    await ctx.send('🎲恭喜'+str(ctx.author.name)+'獲得1顆寶石')
                    self.gem[ctx.author.name] = int(self.gem[ctx.author.name])+1
                    self.guess = 0
                    self.save_gem()  
                    return 
                if((int)(reply.content)>((int)(high)) or (int)(reply.content)<((int)(low))):
                    tmp = '答案介於'+str(low)+'和'+str(high)+'之間'
                elif((int)(reply.content)<answer):
                    low = reply.content
                elif((int)(reply.content)>answer):
                    high = reply.content
                tmp = '答案介於'+str(low)+'和'+str(high)+'之間'
                await ctx.send(tmp) 
                number = number + 1
        self.guess = 0    
        await ctx.send('🎲請再接再厲，'+str(ctx.author.name))  
    
    
    @commands.command()
    async def g_21(self,ctx):
        if(self.g_21 == 1):
            await ctx.send('🎲已經有人正在遊玩，請稍後再試')
            return  
        
        await ctx.send(embed=self.g_21_des)   
        self.g_21 = 1     
        num = 0
        result = list()
        val = random.randint(1,13)
        A_num = 0
        if(val == 1):
            result.append('A')
            A_num = 1
            num = num + 1
        if(2<=val and val<=10):
            num = num+val
            result.append(str(val))
        if(val==11):
            num = num + 10
            result.append('J')
        if(val==12):
            num = num + 10
            result.append('Q')
        if(val==13):
            num = num + 10
            result.append('K')    
        await ctx.send('🎲目前牌型:'+str(result)+'請問你是否要繼續？(Y=是，N=否)')
        while(num<=21):
            reply = await self.bot.wait_for('message')
            if(reply.author.name == ctx.author.name and reply.content=='Y' ):
                val = random.randint(1,13)
                if(val == 1):
                    result.append('A')
                    A_num = 1
                    num = num + 1
                if(2<=val and val<=10):
                    num = num+val
                    result.append(str(val))
                if(val==11):
                    num = num + 10
                    result.append('J')
                if(val==12):
                    num = num + 10
                    result.append('Q')
                if(val==13):
                    num = num + 10
                    result.append('K') 
                await ctx.send('🎲目前牌型:'+str(result)+'請問你是否要繼續？(Y=是，N=否)')   
            if(reply.author.name == ctx.author.name and reply.content=='N'):
                break
        
        bot_num = random.randint(16,24)
        if(A_num == 1 and num<=11):
            num = num + 10

        await ctx.send('🎲您的點數：'+str(num)+'/BOT的點數：'+str(bot_num))
        
        if(num <=21 and bot_num<=21):
            if(num < bot_num):
                output_str = '🎲請再接再厲，'+str(ctx.author.name) 
            elif(num == bot_num):
                output_str = '🎲此局平手'
            else:
                output_str = '🎲恭喜'+str(ctx.author.name)+'獲得1顆寶石'
                self.gem[ctx.author.name] = int(self.gem[ctx.author.name])+1
        if(num <=21 and bot_num > 21):
            output_str = '🎲恭喜'+str(ctx.author.name)+'獲得1顆寶石'
            self.gem[ctx.author.name] = int(self.gem[ctx.author.name])+1
        if(num >21 and bot_num <= 21):   
            output_str = '🎲請再接再厲，'+str(ctx.author.name) 
        if(num >21 and bot_num > 21):
            output_str = '🎲此局平手'   
        
        await ctx.send(output_str)
        self.g_21 = 0
        self.save_gem()  
        
    @commands.command()
    async def dice(self,ctx,value):
        name = ctx.author.name
        if(int(value) > int(self.point[name])*0.3 or int(value) < 0 ):
            await ctx.send(str(ctx.author.name)+'，你沒有這麼多錢(單次賭注不能超過現金30%)')
            return
        money = int(self.point[name])
        a = random.randint(1,6)
        b = random.randint(1,6)
        c = random.randint(1,6)
        if(a==b==c):  
            base = math.floor(14-np.log10(money))+0.01*self.gem[name]
            result = int(int(value)*base)
            output_str = '🎲你骰出了豹子[ '+str(a)+' , '+str(b)+' , '+str(c)+' ]，BOT放棄了，恭喜'+str(ctx.author.name)+'獲得'+str(result)+'元\n'
            output_str +='🎲base = '+str(base)
            self.point[ctx.author.name] = int(self.point[ctx.author.name])+result
            await ctx.send(output_str)
            return
        d = random.randint(1,6)
        e = random.randint(1,6)
        f = random.randint(1,6)
        output_str = ''
        output_str +='🎲你骰出了點數 [ '+str(a)+' , '+str(b)+' , '+str(c)+' ]  總點數'+str(a+b+c)+'點'+'\n'
        output_str +='🎲BOT骰出了點數 [ '+str(d)+' , '+str(e)+' , '+str(f)+' ]  總點數'+str(d+e+f)+'點'+'\n'                  
        base = 0
        if(d==e==f):
            base = 3
            output_str += '🎲BOT骰出了豹子'+str(ctx.author.name)+'失去了'+str(int(value)*base)+'元\n'
            self.point[ctx.author.name] = int(self.point[ctx.author.name])-int(value)*base      
        elif((a+b+c) == 10):
            base = math.floor(13-np.log10(money))+0.01*self.gem[name]
            result = int(int(value)*base)
            output_str += '🎲恭喜'+str(ctx.author.name)+'獲得'+str(result)+'元\n'
            self.point[ctx.author.name] = int(self.point[ctx.author.name])+result   
        elif((d+e+f) == 10):
            base = 2
            output_str += '🎲'+str(ctx.author.name)+'失去了'+str(int(value)*base)+'元\n'  
            self.point[ctx.author.name] = int(self.point[ctx.author.name])-int(value)*base
        elif((a+b+c)%10 < (d+e+f)%10):
            base = 1
            output_str += '🎲'+str(ctx.author.name)+'失去了'+str(value)+'元\n'  
            self.point[ctx.author.name] = int(self.point[ctx.author.name])-int(value)
        else:
            base = math.floor(12-np.log10(money))+0.01*self.gem[name]
            result = int(int(value)*base)
            output_str += '🎲恭喜'+str(ctx.author.name)+'獲得'+str(result)+'元\n'
            self.point[ctx.author.name] = int(self.point[ctx.author.name])+result 
        output_str += '🎲base = '+str(base)
        await ctx.send(output_str)

    @commands.command()        
    async def rescue(self,ctx):
        money =  int(self.point[ctx.author.name])
        if(money<1000):
            self.point[ctx.author.name] = int(1000)

def setup(bot):
    bot.add_cog(member(bot))
