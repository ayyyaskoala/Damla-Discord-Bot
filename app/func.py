from tkinter import Variable
import discord, requests,json, random ,sqlite3
from discord.ext import commands
 
import requests,time,datetime
from bs4 import BeautifulSoup
 

database_path = "app/data/database.db"

#-------Günün Sözü-----------------------------------------
def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return (quote)
#-------IMDB Movies Query/Add/--------------------------------
def film_imdb_sorgula(link,user):
  response = requests.get(link)
  html_content = response.content

  soup = BeautifulSoup(html_content,"html.parser")
  film_existis = False
  
  try:
    error = soup.find("div",{"class":"error_bubble"})
    print(error.text)  
    film_existis = False
    return "Böyle bir film bulunmamakta"
  except:
    film_existis = True  
  
  if film_existis:
    json_icerik = soup.find("script",{"type":"application/ld+json"})
    data = str(json_icerik.next_element)
    
    veri = json.loads(data)
    
    try:
      FilmTarzi = veri["@type"]
    except:
      FilmTarzi = "Belirsiz Tarz'da"

    needed_info = ["name","url","image","description","datePublished","genre"] #all i want 

    for key in needed_info:
      if key in veri.keys():  
          exec(f'global {key} ; {key} = veri["{key}"]')   #key = veri[key]   -> needed_info'e göre 
      else:
        exec(f'global {key} ; {key} = "Veri Yok"')       #key = "Veri Yok"  -> needed_info'e göre 

    if "genre" in globals():
      if type(veri["genre"]) == list:
        temp_str = ""
        for i in veri["genre"]:
          temp_str += i +" ,"
      genre = temp_str

    
    #name = veri["name"]
    return film_veri_ekle(name,url,image,description,datePublished,genre,user,FilmTarzi)
def film_veri_ekle(name,url,image,description,datePublished,genre,user,FilmTarzi):  
    con = sqlite3.connect(database_path)
    cursor = con.cursor()  
    cursor.execute('CREATE TABLE IF NOT EXISTS "filmler" ("id" TEXT,"name" TEXT,"url" TEXT,"image" TEXT,"description" TEXT,"datePublished" TEXT,"genre" TEXT,"user" TEXT)')
    cursor.execute("SELECT * FROM filmler WHERE url = ?",(url,))
    temp_data = cursor.fetchall()

    if len(temp_data) == 0:
      id = len(cursor.execute("SELECT * FROM filmler").fetchall()) + 1
      cursor.execute("INSERT INTO filmler (id,name,url,image,description,datePublished,genre,user) VALUES (?,?,?,?,?,?,?,?)",(id,name,url,image,description,datePublished,genre,user))
      con.commit()    
      return  "Seçilen " + FilmTarzi +" "+user+" adına veri tabanına eklendi"
    else:
      return "Veri önceden eklenmiş!!" 
def film_veri_listele():
  cursor = sqlite3.connect(database_path).cursor()
  cursor.execute('SELECT * FROM filmler')
  data = cursor.fetchall()

  return data
#----Günün Nasıl geçiyor sorusu----------
def nasilsin_veri_cek():
  cursor = sqlite3.connect(database_path).cursor()
  cursor.execute('SELECT * FROM nasilsin')
  data = cursor.fetchall()
  return data
#------Borsalar-*-----------
def borsa():
  class crypto():
    def __init__(self,symbol,volume,high,low,bid):
        self.symbol = symbol
        self.volume = volume 
        self.high = high
        self.low = low
        self.bid = bid

  data = requests.get("https://www.mxc.com/open/api/v2/market/ticker")
  data_json = json.loads(data.text)

  for i in data_json["data"]:
    x = str(i).lower()

    if "ame_usdt" in x:
      ame = crypto(i["symbol"],i["volume"],i["high"],i["low"],i["bid"])   

    if "vet_usdt" in x:
      vet = crypto(i["symbol"],i["volume"],i["high"],i["low"],i["bid"])    
  
    if "xrp_usdt" in x:
      xrp = crypto(i["symbol"],i["volume"],i["high"],i["low"],i["bid"])  
    
    if "eth_usdt" in x:
      eth = crypto(i["symbol"],i["volume"],i["high"],i["low"],i["bid"])  
    
    
  return ame,vet,xrp,eth
#-----Kullanıcı Düzenlemessi-*-----------
def user_duzenle(user):
  id = ""
  sayi = ["0","1","2","3","4","5","6","7","8","9"]
  for i in user:
    if i in sayi:
      id += i
  return id
#-----Damla Sözleri ------------------
def damla_sozu_ekle(from_user,to_user,date):   
  con = sqlite3.connect(database_path)
  cursor = con.cursor()
                                              
  cursor.execute("CREATE TABLE IF NOT EXISTS damla_sozler(from_user TEXT,to_user TEXT,date DATE)")
  con.commit()
  
  cursor.execute("INSERT INTO damla_sozler VALUES(?,?,?)",(from_user,to_user,date))
  con.commit()  

  print(str(from_user)+"'dan ",str(to_user)+"'a damla sözü eklenmiştir")
def damla_sozu_sorgula(*data):
  way = data[0]
  if way == 1:
    to_user = data[1]
  elif way == 2:
    from_user = data[1]

  con = sqlite3.connect("data/database.db")
  cursor = con.cursor()

  if way == 1:
    cursor.execute("SELECT * FROM damla_sozler where to_user = ?",(to_user,))    
    data = cursor.fetchall()
    return data
  elif way==2 :
    cursor.execute("SELECT * FROM damla_sozler where from_user = ?",(from_user,))    
    data = cursor.fetchall()
    return data
#-----Köfte Sözleri ------------------
def kofte_soz_ekle(from_user,to_user,date_now):   
  con = sqlite3.connect(database_path)
  cursor = con.cursor()
                                              
  cursor.execute("CREATE TABLE IF NOT EXISTS kofte_sozler(from_user TEXT,to_user TEXT,date DATE)")
  con.commit()
  
  cursor.execute("INSERT INTO kofte_sozler VALUES(?,?,?)",(from_user,to_user,date_now))
  con.commit()  
def kofte_sozu_sorgula(*data):
  way = data[0]
  if way == 1:
    to_user = data[1]
  elif way == 2:
    from_user = data[1]

  con = sqlite3.connect(database_path)
  cursor = con.cursor()

  if way == 1:
    cursor.execute("SELECT * FROM kofte_sozler where to_user = ?",(to_user,))    
    data = cursor.fetchall()
    return data
  elif way==2 :
    cursor.execute("SELECT * FROM kofte_sozler where from_user = ?",(from_user,))    
    data = cursor.fetchall()
    return data
#-----FredBotKayıt------------------
def fredBotPlayer(msg):
  if "added " in msg:
    try:
      text = msg.split("added")
      username = text[0]
      musicName = text[1]

      
      con = sqlite3.connect(database_path)
      cursor = con.cursor()
      cursor.execute('CREATE TABLE IF NOT EXISTS "music" ("userName" TEXT,"musicName" TEXT,"currentTime" TEXT)')
      cursor.execute("INSERT INTO music (userName,musicName,currentTime) VALUES (?,?,?)",(username,musicName,time.time()))
      con.commit()
    except:
      return"hata meydana geldi"
    else:
      return "Veri tabanına kayıt başarılı"
    
     
  return "ekleme işlemi yok"
#-----Random-----------------------
def randomUser(memberList):
    random.shuffle(memberList)
    count = len(memberList)
    
    if count == 1:
      return False

    if count % 2 == 0:
        no = count/2
        team1 = memberList[:int(no)]
        team2 = memberList[int(no):]
    elif( count % 2 == 1):
        no = (count - 1 ) / 2
        team1 = memberList[:int(no)]
        team2 = memberList[int(no):]

    team1_str = ""
    team2_str = ""

    for i in team1:
        team1_str += "<@!"+str(i)+"> "
    for i in team2:
        team2_str += "<@!"+str(i)+"> "  

    embed = discord.Embed(title="Let The Games Begin",
                          url="https://www.pornhub.com",
                          colour=discord.Colour.red())

    embed.add_field(name="TEAM GAY", value=team1_str, inline="False")      
    embed.add_field(name="TEAM LEZ", value=team2_str, inline="False")

    return embed







