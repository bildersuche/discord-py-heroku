import os

import discord
import messagesxd
client = discord.Client()
client.prefix="-"
message=messages.message
nsg={}
msgs={}
channelmessage = {}
@client.event
async def on_message(msg):
  global msgs,nsg, channelmessage, message
  msg.content=msg.content.lower()
  try:
    nsg[msg.channel.id]+=1
  except:
    nsg[msg.channel.id]=1000
  msg.content=msg.content.lower()
  if "/" in msg.content:
    return
  if "@" in msg.content:
    return
  if "<" in msg.content:
    return
  if "0" in msg.content:
    return
  if "1" in msg.content:
    return
  if "2" in msg.content:
    return
  if "3" in msg.content:
    return
  if "4" in msg.content:
    return
  if "5" in msg.content:
    return
  if "6" in msg.content:
    return
  if "7" in msg.content:
    return
  if "8" in msg.content:
    return
  if "9" in msg.content:
    return
  if client.prefix in msg.content or str(client.user.id) in msg.content:
   if nsg[msg.channel.id]:
    try:
      msg.content=msg.content.replace(client.prefix,"")
      n=0
      for l in range(len(message[msg.content]['count'])):
        if message[msg.content]['count'][l]>n:
          n=message[msg.content]['count'][l]
          print(message[msg.content]['count'][l])
      for l in range(len(message[msg.content]['count'])):
        if message[msg.content]['count'][l]==n:
          msgs[msg.id]=message[msg.content]['msg'][l]
      if not msg.author.bot:
        await msg.channel.send(msgs[msg.id])
      print(msg.content+"===>"+msgs[msg.id])
      channelmessage[msg.channel.id]=msgs[msg.id]
      pass
    except:
      zok=[]
      for l in message:
        ten=0
        nch=l
        for letter in msg.content:
          if letter in nch:
            nch=nch.replace(letter,"")
            ten+=1
        zok.append(ten)
      oldnumber=0
      for number in zok:
        if zok[number] >= zok[oldnumber]:
          oldnumber=number
      t=0
      for n in message:
        if t==oldnumber:
          msg.content=n
        t+=1
      try:
        msg.content=msg.content.replace(client.prefix,"")
        n=0
        for l in range(len(message[msg.content]['count'])):
          if message[msg.content]['count'][l]>n:
            n=message[msg.content]['count'][l]
            print(message[msg.content]['count'][l])
        for l in range(len(message[msg.content]['count'])):
          if message[msg.content]['count'][l]==n:
            msgs[msg.id]=message[msg.content]['msg'][l]
        if not msg.author.bot:
          await msg.channel.send(msgs[msg.id])
        print(msg.content+"===>"+msgs[msg.id])
        channelmessage[msg.channel.id]=msgs[msg.id]
        pass
      except:
        pass


    try:
      msg.content=msg.content.replace(client.prefix,"")
      n=0
      for l in range(len(message[channelmessage[msg.channel.id]]["msg"])):
        if message[channelmessage[msg.channel.id]]['msg'][l]==msg.content:
          message[channelmessage[msg.channel.id]]['count'][l]+=1;
          d=open("messages.py","w")
          d.write("message="+str(message))
          d.close()
          channelmessage[msg.channel.id]=msg.content
          return
    except:
      pass
  try:
    
    try:
      message[channelmessage[msg.channel.id]]['msg'].append(msg.content)
      message[channelmessage[msg.channel.id]]['count'].append(1)
    except:
      message[channelmessage[msg.channel.id]]={}
      message[channelmessage[msg.channel.id]]['msg']=[msg.content]
      message[channelmessage[msg.channel.id]]['count']=[1]
    d=open("messages.py","w")
    d.write("message="+str(message))
    d.close()
    
    channelmessage[msg.channel.id]=msg.content
      
  except:
    channelmessage[msg.channel.id]=msg.content

TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    client.run(TOKEN)
