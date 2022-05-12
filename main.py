import os
 
from app import *
from app.func import *

from app.keep_alive import keep_alive

from app.Commands import damla,netflix,delete,random,cfg
from app.Events import onReady,onMessageEvents

client = commands.Bot(command_prefix="!",intents = intents)

client.add_cog(netflix(client)) #send netflix password
client.add_cog(delete(client))  #delete message from channel
client.add_cog(damla(client))   #buy ur friends damla for tonight
client.add_cog(random(client))  #create random team
client.add_cog(cfg(client))     #sends CsGo cfg file

client.add_cog(onReady(client)) #just runing in the beggining
client.add_cog(onMessageEvents(client)) #answering on specific messages

if __name__ == "__main__":
    API_KEY = os.environ['APIDamla']
    keep_alive()
    client.run()  




  
  
  
  
  
  
  

