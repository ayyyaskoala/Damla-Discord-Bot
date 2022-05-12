from discord.ext import commands
from app.func import *

import discord, asyncio ,os

 
class netflix(commands.Cog,name="Netflix Login Request"):
    def __init__(self,client:commands.Bot):
        self.client = client
        self.netflixUsers = [2970000000000002960,297000000000000317,4900000000000080,3170000000000000424] #UserID of my Family
        self.link = "https://www.netflix.com/tr-en/login"
    
    @commands.command()
    async def netflix(self,ctx:commands.Context):
        if ctx.author.id in self.netflixUsers:
            myMail = os.environ['NetflixEmail']
            password = os.environ['NetflixPassword']
          
            embed = discord.Embed(title="Netflix Login")
            embed.add_field(name="username", value=myMail, inline="False")      
            embed.add_field(name="password", value=password, inline="False")
            myMessage = await ctx.author.send(embed=embed)    
            await asyncio.sleep(2)

            embed = discord.Embed(title="after 8 sec password will hide....")
            embed.add_field(name="username", value=myMail, inline="False")      
            embed.add_field(name="password", value=password, inline="False")
            await myMessage.edit(embed=embed)
            await asyncio.sleep(3)

            embed = discord.Embed(title="hmm or just in 5....")
            embed.add_field(name="username",value=myMail, inline="False")      
            embed.add_field(name="password", value=password, inline="False")
            await myMessage.edit(embed=embed)
            await asyncio.sleep(5)

            embed = discord.Embed(title="Too late.I'm in the dark here....")
            embed.add_field(name="username", value=myMail, inline="False")      
            embed.add_field(name="password", value="******", inline="False")
            await myMessage.edit(embed=embed)
            return
        else:
            await ctx.author.send("You are not member")
        return  

class delete(commands.Cog,name="Delete Message"):
    def __init__(self,client:commands.Bot,*args):
        self.client = client
        self.args = args
    
    @commands.command()
    async def delete(self,ctx:commands.Context,*args):
        if ctx.author.name == "Mr.Koala": #<- that's me :D
            if len(args) == 1:
                try:
                    count = int(args[0])
                    await ctx.channel.purge(limit=count)
                    return
                except:
                    await ctx.send("input must be an Integer")
           
        else:
            ctx.send("Who do you think you are?")     
 
class damla(commands.Cog,name="Damla Borçları Ekleme/Sorgulama"):
    def __init__(self,client:commands.Bot,*args):
        self.client = client
        self.args = args

    @commands.command()
    async def damla(self,ctx:commands.Context,*args):   
        con = sqlite3.connect("app/data/database.db")
        cursor = con.cursor()   

        if args[0] == "ekle":   #!damla ekle @mrkoala 1             
            if "<@" in args[1]:
                kime = user_duzenle(args[1])
            else:
                return await ctx.send("Damla borçlarını sadece bir Kullancıya atılabilir")
            kimden = ctx.author.id
            date = "Null"

            try:
                adet = int(args[2])
            except:
                return await ctx.send("Bir sayı girilmeli")            
                                                        
            cursor.execute("CREATE TABLE IF NOT EXISTS damla_sozler(from_user TEXT,to_user TEXT,date DATE)")            
            for i in range(0,int(adet)):
                cursor.execute("INSERT INTO damla_sozler VALUES(?,?,?)",(kimden,kime,date))
            con.commit()

            return await ctx.send("Damla borçları kayda geçmiştir")
        elif args[0] == "sorgu": #!damla sorgu / !damla sorgu <@userID>
            if len(args) == 1: #!damla sorgu 
                authorID = ctx.author.id    
            if len(args) == 2: #!damla sorgu <@userID>
                authorID = user_duzenle(args[1])
  
            cursor.execute("SELECT * FROM damla_sozler where to_user = ?",(authorID,))    
            borcuOlanlar = cursor.fetchall()
            borcuOlanlarTemp = []

            cursor.execute("SELECT * FROM damla_sozler where from_user = ?",(authorID,))    
            borcluOldugun = cursor.fetchall()
            borcluOldugunTemp = []

            #sana borçlu olanlar
            for i in borcuOlanlar:
                borcuOlanlarTemp.append(i[0])
            #senin borçlu olduğun
            for i in borcluOldugun:
                borcluOldugunTemp.append(i[1])
                        
            borcuOlanlarResult = ""
            for i in set(borcuOlanlarTemp):
                borcuOlanlarResult += "<@" + str(i)+ ">  " + str(borcuOlanlarTemp.count(i)) + "  _|_  "

            borcluOldugunResult = ""
            for i in set(borcluOldugunTemp):
                adet = borcluOldugunTemp.count(i)
                borcluOldugunResult += "<@" + str(i)+ ">  " + str(adet) + "  _|_  "


            #sayma algoritması 
            if len(borcuOlanlarResult) == 0 :
                borcuOlanlarResult="Bulunamadı"
            if len(borcluOldugunResult) == 0:
                borcluOldugunResult = "Bulunamadı"

            embed=discord.Embed(title="Damla Borçları")
            embed.add_field(name="Sana Borcu olanlar", value=borcuOlanlarResult, inline=False)
            embed.add_field(name="Senin Borçlu oldukların", value=borcluOldugunResult, inline=False)
            await ctx.send(embed=embed)
        else:
            return await ctx.send("Hatalı Kullanım var")
  
class random(commands.Cog,name="Create Random Team"):
    def __init__(self,client:commands.Bot):
        self.client = client

    @commands.command()
    async def random(self,ctx:commands.Context):   
        try:
            memberList = list(ctx.author.voice.channel.voice_states.keys())
            embed = randomUser(memberList)    
            if embed:
                await ctx.channel.send(embed=embed)
            else:
                await ctx.channel.send("play on your own")
        except AttributeError:
            await ctx.channel.send("First join a Room")                        

class cfg(commands.Cog,name="CS:GO cfg"):
    def __init__(self,client:commands.Bot):
        self.client = client

    @commands.command()
    async def cfg(self,ctx:commands.Context):  
        await ctx.send(file=discord.File('app/data/cfg/koala.txt'))
        return




            







