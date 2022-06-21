from discord.ext import commands
from app.func import *

import discord, asyncio ,os, sqlite3 as sql
 

 
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
            await ctx.author.send("You are no member")
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

        if args[0] == "add":   #!damla add @mrkoala 1             
            if "<@" in args[1]:
                kime = user_duzenle(args[1])
            else:
                return await ctx.send("It must be a user....")
            kimden = ctx.author.id
            date = "Null"

            try:
                adet = int(args[2])
            except:
                return await ctx.send("It must be INT")            
                                                        
            cursor.execute("CREATE TABLE IF NOT EXISTS damla_sozler(from_user TEXT,to_user TEXT,date DATE)")            
            for i in range(0,int(adet)):
                cursor.execute("INSERT INTO damla_sozler VALUES(?,?,?)",(kimden,kime,date))
            con.commit()

            return await ctx.send("Damla borçları kayda geçmiştir")

        elif args[0] == "request": #!damla request / !damla request <@userID>
            if len(args) == 1: #!damla request 
                authorID = ctx.author.id    
            if len(args) == 2: #!damla request <@userID>
                authorID = user_duzenle(args[1])
  
            cursor.execute("SELECT * FROM damla_sozler where to_user = ?",(authorID,))    
            borcuOlanlar = cursor.fetchall()
            borcuOlanlarTemp = []

            cursor.execute("SELECT * FROM damla_sozler where from_user = ?",(authorID,))    
            borcluOldugun = cursor.fetchall()
            borcluOldugunTemp = []

            #who owe you
            for i in borcuOlanlar:
                borcuOlanlarTemp.append(i[0])
            #who you owe
            for i in borcluOldugun:
                borcluOldugunTemp.append(i[1])
                        
            borcuOlanlarResult = ""
            for i in set(borcuOlanlarTemp):
                borcuOlanlarResult += "<@" + str(i)+ ">  " + str(borcuOlanlarTemp.count(i)) + "  _|_  "

            borcluOldugunResult = ""
            for i in set(borcluOldugunTemp):
                adet = borcluOldugunTemp.count(i)
                borcluOldugunResult += "<@" + str(i)+ ">  " + str(adet) + "  _|_  "


            #counting... 
            if len(borcuOlanlarResult) == 0 :
                borcuOlanlarResult="Bulunamadı"
            if len(borcluOldugunResult) == 0:
                borcluOldugunResult = "Bulunamadı"

            embed=discord.Embed(title="Damla Borçları")
            embed.add_field(name="who owe you", value=borcuOlanlarResult, inline=False)
            embed.add_field(name="who you owe", value=borcluOldugunResult, inline=False)
            await ctx.send(embed=embed)
        else:
            return await ctx.send("Failed....")
  
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

class TimeCounter(commands.Cog,name="TimeCounter"):
    def __init__(self,client:commands.Bot):
        self.client = client

    @commands.command()
    async def timeCounter(self,ctx:commands.Context):  
        MemberID = ctx.author.id

        con = sql.connect("app/data/database.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM connectionCounter WHERE memberId=?",(MemberID,))
        data = cursor.fetchall()
        
        if len(data)!=0:
            data = data[0]
            inSecond = int(data[2])
            inMinutes = int(inSecond/60)
            inHours = int(inMinutes/60)

            if inHours>0:
                #result = "Cücelerin Diyarında **{} saatini** heba etmişsin.".format(inHours)
                result = "You spent **{} Hours** in Dwarf's World.".format(inHours)
            elif inMinutes>0:
                result = "You spent **{} Minutes** in Dwarf's World.".format(inMinutes) 
            else:
                result = "You look quite new here...just join fun will find you"  

            await ctx.send(result)
        
        else:           
            await ctx.send("Just reconnect to the channel")   
        return

class KaloriCounter(commands.Cog,name="KaloriCounter"):
    def __init__(self,client:commands.Bot):
        self.client = client

    @commands.command()
    async def yemek(self,ctx:commands.Context):  
            #Kontrol işlemi için gerekli bir fonksiondur
            MyChannel = ctx.channel
            def check(m):
                return m.channel == MyChannel
            embedFields = [
                ["kalori","kalori","False"],
                ["protein","protein","True"],
                ["karbonhidrat","karbonhidrat","True"],
                ["yag","yag","True"],
                ["Toplam Gramaj","Toplam Gramaj","False"]
            ] 
            #Tüm embedler Buraya kayıt edilip en son işleniyor 
            embedSaver = []   
            #Toplamları Kalori Buraya Kayıt olacak
            ToplamSonuclarim = {
                "kalori" : 0,
                "protein" : 0,
                "karbonhidrat" : 0,
                "yag" : 0,
                "Toplam Gramaj" : 0  ,
                "yemek_isim_gramaj_bilgisi" : ""
            } 

            #öğünü belirle                  
            infoMessage = await ctx.send("Kahvaltı = 1\nAkşam Yemeği = 2\nAtıştırmalık = 3\n**Hangi öğünü kayıt edeceksen onun sayısını gir**")
            userInput = await self.client.wait_for('message',check=check, timeout=60)
            ogun_adi = ["Kahvaltı","Akşam Yemeği","Atıştırmalık"][int(userInput.content)-1]

            if ogun_adi == "Kahvaltı":
                pass
                await infoMessage.edit(content="Standart Kahvaltı ise = 1 \nManuell olarak bilgileri girmek istersen = 2")
                userInput = await self.client.wait_for('message',check=check, timeout=60)
                if userInput == "1":
                    pass #veri tabanında yulaf muz ... verileri çek
                #aksi takdirde kcal'ler elle girelecek
            elif ogun_adi == "Akşam Yemeği":
                pass #kcal'ler elle girelecek
            elif ogun_adi == "Atıştırmalık":
                await infoMessage.edit(content="Kayıtlı Atıştırmalıklara göz at")
                #elle girilmesi kolay-> ismi & kcal
            
            
            #Yemekleri oluşturmak için Döngü
            while True:
                embedTEMP = discord.Embed(title="Yemekler Burada görünecek...")
                myEmbedMessage2 = await ctx.send(embed=embedTEMP)
                infoMessage2 = await ctx.send(".............")

                await infoMessage2.edit(content="Yediğin gıdanın adını buraya girer misin?")
                userInput = await self.client.wait_for('message',check=check, timeout=60)

                embedTEMP.title = userInput.content
                embedTEMP.description = ogun_adi
                await myEmbedMessage2.edit(embed=embedTEMP)

                #Verilerin önceden kaydedilip edilmediğine bak                
                SQLFetch = SQLyemekSorgusu(str(userInput.content.lower()))
                
                if len(SQLFetch) > 0: #Eğer yemek veri tabanında varsa orda çekilecek 
                    islem = False #Daha Önceden Kayıt Edilmiş
                    embedFieldsTemp = [
                        ["kalori",SQLFetch[0][2],"False"],
                        ["protein",SQLFetch[0][3],"True"],
                        ["karbonhidrat",SQLFetch[0][4],"True"],
                        ["yag",SQLFetch[0][5],"True"],                
                        ["Toplam Gramaj",0,"False"]
                    ]

                    for x,y,z in embedFieldsTemp:                        
                        if x == "Toplam Gramaj":
                            await infoMessage2.edit(content="Toplam kaç gram yediğini gir") 
                            userInput = await self.client.wait_for('message',check=check, timeout=60)
                            embedTEMP.add_field(name=x, value=str(userInput.content), inline=z)
                            continue
                        embedTEMP.add_field(name=x, value=str(y), inline=z) 

                    await myEmbedMessage2.edit(embed=embedTEMP) 

                else: #yoksa elle girilmesi gerekiyor
                    islem = True  #Yeni Kayıt Edildi
                    for x,_,z in embedFields:
                        if x == "Toplam Gramaj":
                            await infoMessage2.edit(content="Toplam kaç gram yediğini gir") 
                            userInput = await self.client.wait_for('message',check=check, timeout=60)
                        else:
                            await infoMessage2.edit(content= x.upper() + " bilgilerini 100gr için gir. En son toplam Gramaj istenilecek") 
                            userInput = await self.client.wait_for('message',check=check, timeout=60)             

                        embedTEMP.add_field(name=x, value=userInput.content, inline=z)
                    
                    await myEmbedMessage2.edit(embed=embedTEMP) 

                await infoMessage2.edit(content="Kayıt işlemine geçmek için q\nBaşka yemek eklemek için w\nBunu silmek için r yaz") 
                userInput = await self.client.wait_for('message',check=check, timeout=60)

                if userInput.content == "q" : 
                    embedSaver.append([embedTEMP,islem])
                    break
                elif userInput.content == "w":
                    embedSaver.append([embedTEMP,islem])
                elif userInput.content == "r":
                    continue    #kayıt etmeden devam ediyorum
                else:
                    embedSaver.append([embedTEMP,islem])
                    await ctx.send("Farklı Tuşa Bastın, yine de kayıt edeceğim")
            

            for i,u in embedSaver: # u = islem
                yemek_adi = i.title
                ogun_adi = i.description

                toplamGramaj = checkFloat(i.fields[4].value )
                ToplamSonuclarim["Toplam Gramaj"] += float(toplamGramaj)                 

                kalori = checkFloat(i.fields[0].value)
                ToplamSonuclarim["kalori"] += float(kalori) * float(toplamGramaj) * 0.01

                protein = checkFloat(i.fields[1].value)
                ToplamSonuclarim["protein"] += float(protein) * float(toplamGramaj) * 0.01

                karbonhidrat = checkFloat(i.fields[2].value )
                ToplamSonuclarim["karbonhidrat"] += float(karbonhidrat) * float(toplamGramaj) * 0.01

                yag = checkFloat(i.fields[3].value)
                ToplamSonuclarim["yag"] += float(yag) * float(toplamGramaj) * 0.01

                yemek_isim_gramaj_bilgisi = str(yemek_adi) + "_" + str(toplamGramaj)  + "_gr | "
                ToplamSonuclarim["yemek_isim_gramaj_bilgisi"] += yemek_isim_gramaj_bilgisi


                if u: #yeni kayıtsa u True'dur ve veri tabanına kayıt yapılır
                    data = (str(ctx.author.name),yemek_adi,kalori,protein,karbonhidrat,yag,str(date.today()))
                    SQLyemekVeriler(data)#ilk defa giirlen gıdaları kaydeder
         

            #Eklenen her şey burada gözükecek
            embedSUM = discord.Embed(title="Bu öğün için senin sonuçların aşaığda listelenecek")
            embedSUM.description = ogun_adi

            for x,y,z in embedFields:
                embedSUM.add_field(name=x, value=ToplamSonuclarim[x], inline=z)
                
            data = (str(ctx.author.name),str(ctx.author.id),str(ogun_adi),str(ToplamSonuclarim["kalori"]),str(ToplamSonuclarim["protein"]),str(ToplamSonuclarim["karbonhidrat"]),str(ToplamSonuclarim["yag"]),str(ToplamSonuclarim["yemek_isim_gramaj_bilgisi"]),str(date.today()))
            SQLkaloriToplami(data) #verileri 'kaloriToplami' içine kayıt eder

            await ctx.send("Veriler Başarıyla Kayıt edilmiştir",embed=embedSUM)

class KaloriResult(commands.Cog,name="KaloriResult"):
    def __init__(self,client:commands.Bot):
        self.client = client

    @commands.command()
    async def yemeksonuc(self,ctx:commands.Context):    
        SQLFetch = kaloriVerileriTopla() 
        toplam = {}

        SUMkalori = 0
        SUMprotein = 0
        SUMkarbonhidrat = 0
        SUMyag = 0

        lastDate = SQLFetch[0][8] #start date watcher

        for i in SQLFetch:
            kalori = checkFloat(i[3])
            protein = checkFloat(i[4])
            karbonhidrat = checkFloat(i[5])
            yag = checkFloat(i[6])
            tarih = i[8]    

            if tarih == lastDate: #aynı günde oldu
                SUMkalori += kalori
                SUMprotein += protein
                SUMkarbonhidrat += karbonhidrat
                SUMyag += yag

                oranlar = OranHesaplama(SUMprotein,SUMkarbonhidrat,SUMyag)

                toplam[tarih] = {
                    "kalori" : SUMkalori,
                    "protein" : SUMprotein,
                    "karbonhidrat" : SUMkarbonhidrat,
                    "yag" : SUMyag,
                    "oran" : oranlar
                }
                
            else: #farklı gün        
                lastDate = tarih
                SUMkalori = kalori
                SUMprotein = protein
                SUMkarbonhidrat = karbonhidrat
                SUMyag = yag
                
                oranlar = OranHesaplama(SUMprotein,SUMkarbonhidrat,SUMyag)
                
                toplam[tarih] = {
                    "kalori" : SUMkalori,
                    "protein" : SUMprotein,
                    "karbonhidrat" : SUMkarbonhidrat,
                    "yag" : SUMyag,
                    "oran" : oranlar
                }
                

        text = ""
        embed = discord.Embed(title="Toplamlar")


        for i in toplam:
            embed.add_field(
                        name=i,
                        value="**KCAL={}  <>  Protein={}  <>  Karbonhidrat={}  <>  Yag={}**".format(toplam[i]["kalori"],toplam[i]["protein"],toplam[i]["karbonhidrat"],toplam[i]["yag"]),
                        inline=False)
            embed.add_field(   
                        name="Oranlar",                     
                        value="**Protein={}%  <>  Karbonhidrat={}%  <>  Yag={}%**".format(toplam[i]["oran"][0],toplam[i]["oran"][1],toplam[i]["oran"][2]),
                        inline=False)

            #text += "Tarih:{} <> KCAL:{} <> Protein:{} <> Karbonhidrat:{} <> Yag:{} \n".format(i,toplam[i]["kalori"],toplam[i]["protein"],toplam[i]["karbonhidrat"],toplam[i]["yag"])
            #text += "Tarih:{} <> Protein:{}% <> Karbonhidrat:{}% <> Yag:{}% \n\n".format(i,toplam[i]["oran"][0],toplam[i]["oran"][1],toplam[i]["oran"][2])


        

         

        await ctx.send(embed=embed)
        





            







