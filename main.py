import os
 
from app import *
from app.func import *

from app.keep_alive import keep_alive

from app.Commands import *
from app.Events import *

client = commands.Bot(command_prefix="!",intents = intents)

client.add_cog(netflix(client)) #will send your netflix password 
client.add_cog(delete(client))  #delete message from channel
client.add_cog(damla(client))   #buy ur friends damla for tomorrow tonight
client.add_cog(random(client))  #create random team(works for people in same channel)
client.add_cog(cfg(client))     #sends CsGo cfg file
client.add_cog(TimeCounter(client))  #how much time you spent in the channel
client.add_cog(KaloriCounter(client))
client.add_cog(KaloriResult(client))

client.add_cog(onReady(client)) #just runing in the beggining
client.add_cog(onMessageEvents(client)) #answering on specific messages
client.add_cog(onMemberUpdate(client)) 

if __name__ == "__main__":
    API_KEY = os.environ['APIKEY']
    keep_alive() #u need keep_alive if u are using Replit or the bot shuts in 30 minutes.
    client.run()  




  
  
  
  
  
  
  

