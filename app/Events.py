from discord.ext import commands
from discord.channel import TextChannel,DMChannel
import discord, asyncio
import random as rd

from app.func import *


class onReady(commands.Cog,name="onReady"):
    def __init__(self,client:commands.Bot):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("U're online. Welcome {0.user}".format(self.client))
        await self.client.change_presence(status=discord.Status.idle,activity=discord.Game('With her no Existing dick'))
        
        global dwarfs_server_object
        global role_of_bots

        dwarfs_server_object = discord.utils.get(self.client.guilds, id = 540000000000000655)      #Dwarf's World <- My Discord Server   
        return
    
class onMessageEvents(commands.Cog,name="onMessageEvents"):
    def __init__(self, client:commands.Bot):
        self.client = client    
        self.damla_nikname = ["damla", "damlacım", "damlacık", "damloş"]
        self.kufur_icerik = ["fuck","bitch","hoe","amk", "aq", "amına", "sik", "siktir", "sikeyim"]
        self.nasilsin_icerik = ["Whats up","nasılsın", "naber"]
        self.merhabalar = ["hi","hello"]
        self.ozlu_sozler = ["word of the day","özlü sözler","özlü söz", "günün sözü", "damla damlat bir söz"]
        self.oyunlar = ["lol", "apex", "cs ", "cs go"]
        self.sevgi = [" ...oyundan önce sakso?","de beni önce bi aşıla","ama önce meme saksosu?"]
        self.deniz_orospu = ["denize açıl", "sea of thieves"]
     
    @commands.Cog.listener()
    async def on_message(self, message):
        if(isinstance(message.channel,TextChannel)):
            #if user is bot 
            if message.author.bot: 
                if message.author.id == 184405311681986560: #FredBot
                    print(fredBotPlayer(message.content))
                return False  
            #Whats up ???!!!
            if any(word in message.content for word in self.nasilsin_icerik) and any(word in message.content for word in self.damla_nikname):
                data = nasilsin_veri_cek()
                i = rd.randrange(0, len(data))
                await message.channel.send(data[i - 1][1])
                return
            #Hello
            if any(word in message.content for word in self.merhabalar) and any(word in message.content for word in self.damla_nikname):
                await message.channel.send("Merhaba Tatlım")
                return
            #profanity $$$$$    
            if any(word in message.content for word in self.kufur_icerik):
                if message.author.name == "Timo":
                    await message.channel.send("Fuck u Timo")
                    return
                else:
                    yazi = "Asıl Ben senin amına koyayım, " + message.author.name + "!"
                    await message.channel.send(yazi)
                    return
            #word of the day
            if any(word in message.content for word in self.ozlu_sozler):
                await message.channel.send(get_quote())
                return
            #gameblabla...
            if any(word in message.content for word in self.oyunlar):
                answer = "Geldim{}".format(random.choice(self.sevgi))
                await message.channel.send(answer)
                return
            #Sea of Thieves
            if any(word in message.content for word in self.deniz_orospu):
                await message.channel.send("Kaptanım denizde az eğlence ister misiniz?")
                return
            #-----Otoma. Role Giving ------    
            ##if someone write !play in the wrong place##
            if "!play" in message.content or "?play" in message.content or "+play" in message.content:
                if message.channel.id == 572300000000000657 or message.channel.id == 9610000000894:          
                    return #written in right place
                else:
                    dwarfs_server_object = discord.utils.get(self.client.guilds, id = 548000000000655)
                    role = discord.utils.get(dwarfs_server_object.roles, id = 5720000000007956)

                    await message.channel.send("U got caught idiot!")
                    await message.author.send("I just wanted to remind you that you are stupid.")
                    await message.author.send("https://fredboat.com/music-player/5480000000000655")
                                        
                    await message.author.add_roles(role)  
            #--------IMDB veri işleme-----------------
            #Add movies to database
            if message.content.startswith("https://www.imdb.com/title"):          
                user = message.author.name
                link = message.content
                veri = film_imdb_sorgula(link, user)    
                await message.author.send(veri)
                return        
            #Film Suggestion
            if message.content == "damla movie":
                data = film_veri_listele()
                film_sayisi = len(data)
                random_sayi = rd.randrange(0, film_sayisi)
                data = data[random_sayi]
                tarih = str(data[5])
                user = data[6]

                embed = discord.Embed(title=data[1] + "(" + tarih[0:4] + ") [" +
                                    str(data[0]) + "/" + str(film_sayisi) + "]",
                                    url="https://www.imdb.com" + data[2],
                                    description=data[4],
                                    colour=discord.Colour.red())

                embed.set_image(url=data[3])
                #embed.add_field(name="Toplam Film Sayısı:", value=str(film_sayisi),inline=True)
                embed.set_footer(text="Film'i ekleyen şahsiyet:" + str(user))

                await message.channel.send(embed=embed)
                return
            #Eklenen Tüm Fimleri Listele
            if message.content == "damla all movies":
                time.sleep(0.3)
                data = film_veri_listele()
                if len(data) > 100:
                    await message.channel.send("there is a limit dude !!")
                    return
                else:
                    embed = discord.Embed(
                        title="Film Listesi",
                        colour=discord.Colour.blue(),
                    )
                    for veri in data:
                        embed.add_field(name=str(veri[0])+". "+veri[1],
                                        value="https://www.imdb.com" +
                                        str(veri[2]),
                                        inline="False")
                    
                    await message.channel.send(embed=embed)
                    return
            #------Damla----------------------------------
            if message.content in self.damla_nikname:
                embed = discord.Embed(
                    title="Merhaba benim adım Damla ",
                    url="https://www.pornhub.com",
                    description="Romanya'nın Moldova Nouă kasabasında hayat buldum. Hayatta kalabilmek için hayat kadını mesleğini öğrendim. İlk başlarda çok zorlandım fakat zamanla genişledim. ",
                    colour=discord.Colour.red())
      
                embed.set_thumbnail(url="https://media.istockphoto.com/photos/picture-of-a-sad-pet-ass-picture-id822753276")               

                embed.add_field(name="Damla Film",
                                value="Eklenen filmlerden bir tanesi listelenir, bok da çıkabilir",
                                inline=True)  
                embed.add_field(name="Film eklemek için",
                                value="IMBD linkini movie'ye ekle",
                                inline=True)
                embed.add_field(name="CFG",
                                value="Kayıtlı tüm CFG dosyaları listelenecek ",
                                inline=True)

                embed.add_field(name="!Damla ekle @username 1",
                                value="Bir Damla ısmarla",
                                inline=True)
                embed.add_field(name="!Damla sorgu @username",
                                value="Damla borçlarını sergiler",
                                inline=True)               
                embed.add_field(name="!Random",
                                value="Rastegele takım oluştur",
                                inline=True) 
              
                embed.add_field(name="özlü sözler",
                                value="Bu günün özlü sözü",
                                inline=True)     
                 

                msg = await message.channel.send(embed=embed)
                await asyncio.sleep(0.8)
                embed.set_thumbnail(url="https://id.metu.edu.tr/wp-content/uploads/2019/04/Layer-21.png")  
                await msg.edit(embed=embed)                
                return
               
            
        if(isinstance( message.channel,DMChannel)):
            if message.content == "help":  
                await message.channel.send("just fuck of")      
                return

            if "fredbot" in message.content:
                await message.channel.send("https://fredboat.com/music-player/500000000000055")
                return
        



   


