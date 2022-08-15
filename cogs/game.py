import discord
from discord.ext import commands
import random

class game_bot(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.count = 0
        self.guess_pwd_channel = 
        self.newnew_channel = 
    
    @commands.Cog.listener()
    async def on_message(self,message):  
        if message.author == self.bot.user:
            return
        if (message.channel.id == self.guess_pwd_channel and self.count == 0 and message.content=='終極密碼'): 
            await message.channel.send('遊戲開始')
            self.count = self.count + 1
            answer = random.randrange(10000)
            low = 0
            high = 10000
            reply = -1
            while(reply!=answer):
                reply = await self.bot.wait_for('message')
                if (reply.content.isdigit() and reply.channel.id == self.guess_pwd_channel):
                    if((int)(reply.content)==answer):
                        await message.channel.send('恭喜！答案正確！答對者:'+(str)(reply.author))
                        low = 0
                        high = 10000
                        self.count = 0
                        await message.channel.send('重新開始，請輸入終極密碼')                       
                        break
                    if((int)(reply.content)>((int)(high)) or (int)(reply.content)<((int)(low))):
                        tmp = '答案介於'+str(low)+'和'+str(high)+'之間'
                    elif((int)(reply.content)<answer):
                        low = reply.content
                    elif((int)(reply.content)>answer):
                        high = reply.content
                    tmp = '答案介於'+str(low)+'和'+str(high)+'之間'
                    await message.channel.send(tmp) 
        if (message.channel.id == self.newnew_channel ):       
            if(message.content=='dice'):
                a = random.randint(1,6)
                await message.channel.send('骰出了點數 '+str(a)+' 點')
            if(message.content=='dice2'):
                a = random.randint(1,6)
                b = random.randint(1,6)
                await message.channel.send('骰出了點數 [ '+str(a)+' , '+str(b)+' ]  總點數'+str(a+b)+'點')
            if(message.content=='dice3'):
                a = random.randint(1,6)
                b = random.randint(1,6)
                c = random.randint(1,6)
                await message.channel.send('骰出了點數 [ '+str(a)+' , '+str(b)+' , '+str(c)+' ]  總點數'+str(a+b+c)+'點')
    
        #await self.bot.process_commands(message)      
            
       
def setup(bot):
    bot.add_cog(game_bot(bot))
    