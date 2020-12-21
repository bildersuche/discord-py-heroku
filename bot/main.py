import os

import discord.ext.commands
import discord
import requests
intents = discord.Intents.default()
intents.members = True
client=discord.ext.commands.Bot(command_prefix=["!z ","z! ","zombie "],intents=intents)
url="https://datas-1.opensourcepy.repl.co"
welcomechannels="zombie"
@client.listen()
async def on_ready():
  print("I am ready")

@client.command()
async def ping(ctx,*args):
  if not args:
    await ctx.send("Pong")
  else:
    msg=""
    for arg in args:
      msg += arg+" "
    await ctx.send("Pong\n> "+msg)

@client.command()
async def invite(ctx):
  await ctx.send("https://discord.com/api/oauth2/authorize?client_id=790227719987134484&permissions=2147483639&scope=bot")

@client.listen()
async def on_member_join(member):
  for channel in member.guild.channels:
    print(channel.name)
    if channel.name in welcomechannels:
      welcomeembed = discord.Embed(color=123456)
      welcomeembed.set_thumbnail(url = member.avatar_url)
      welcomeembed.title=member.display_name
      await channel.create_webhook(name=member.display_name)
      for hook in await channel.webhooks():
        if hook.name == member.display_name:
          await hook.send(embed=welcomeembed,avatar_url=member.avatar_url)
          await hook.delete()

@client.command()
async def info(ctx, user):
  user = ctx.guild.get_member(int(user.replace("<","").replace(">","").replace("@","").replace("!","")))
  rolesofuser=""
  for role in user.roles:
    rolesofuser+=role.name+" - "+str(role.id)+"\n"
  infoembed=discord.Embed(title=user.name,description=rolesofuser)
  infoembed.set_thumbnail(url=user.avatar_url)
  infoembed.set_footer(text="NickName: "+user.display_name)
  await ctx.send(embed=infoembed)

@client.command()
async def thumbnail(ctx, *, arg):
  requests.post(url,data={"id":str(ctx.author.id)+"thumbnail","value":arg})
  await ctx.message.delete()

@client.command()
async def title(ctx, *, arg):
  requests.post(url,data={"id":str(ctx.author.id)+"title","value":arg})
  await ctx.message.delete()

@client.command()
async def color(ctx, *, arg):
  requests.post(url,data={"id":str(ctx.author.id)+"color","value":int(arg)})
  await ctx.message.delete()

@client.command()
async def name(ctx, *, arg):
  requests.post(url,data={"id":str(ctx.author.id)+"name","value":arg})
  await ctx.message.delete()

@client.command()
async def avatar(ctx, *, arg):
  requests.post(url,data={"id":str(ctx.author.id)+"avatar","value":arg})
  await ctx.message.delete()

@client.command()
async def sendi(ctx, image, *,  arg):
  thumbnail = requests.get(url+"/"+str(ctx.author.id)+"thumbnail").text
  title = requests.get(url+"/"+str(ctx.author.id)+"title").text
  color = requests.get(url+"/"+str(ctx.author.id)+"color").text
  name = requests.get(url+"/"+str(ctx.author.id)+"name").text
  avatar = requests.get(url+"/"+str(ctx.author.id)+"avatar").text
  sendembed=discord.Embed(title=title,color=int(color),description=arg)
  sendembed.set_thumbnail(url=thumbnail)
  sendembed.set_image(url=image)
  await ctx.channel.create_webhook(name=name)
  for hook in await ctx.channel.webhooks():
    if hook.name == name:
      await hook.send(embed=sendembed,avatar_url=avatar)
      await hook.delete()
  await ctx.message.delete()

@client.command()
async def send(ctx, *, arg):
  thumbnail = requests.get(url+"/"+str(ctx.author.id)+"thumbnail").text
  title = requests.get(url+"/"+str(ctx.author.id)+"title").text
  color = requests.get(url+"/"+str(ctx.author.id)+"color").text
  name = requests.get(url+"/"+str(ctx.author.id)+"name").text
  avatar = requests.get(url+"/"+str(ctx.author.id)+"avatar").text
  sendembed=discord.Embed(title=title,color=int(color),description=arg)
  sendembed.set_thumbnail(url=thumbnail)
  await ctx.channel.create_webhook(name=name)
  for hook in await ctx.channel.webhooks():
    if hook.name == name:
      await hook.send(embed=sendembed,avatar_url=avatar)
      await hook.delete()
  await ctx.message.delete()

@client.command()
async def set(ctx, name, *, value):
  requests.post(url,data={"id":str(ctx.author.id)+name,"value":value})
  await ctx.message.delete()
@client.command()
async def get(ctx, name):
  value=requests.get(url+"/"+str(ctx.author.id)+name).text
  getembed=discord.Embed(title=ctx.author.name,color=123456,description="Your variable "+name+":\n"+value)
  await ctx.channel.create_webhook(name=ctx.author.display_name)
  for hook in await ctx.channel.webhooks():
    if hook.name == ctx.author.display_name:
      await hook.send(embed=getembed,avatar_url=ctx.author.avatar_url)
      await hook.delete()
  await ctx.message.delete()

@client.command()
async def sendas(ctx, user, *, arg):
  user = ctx.guild.get_member(int(user.replace("<","").replace(">","").replace("@","").replace("!","")))
  await ctx.channel.create_webhook(name=user.display_name)
  for hook in await ctx.channel.webhooks():
    if hook.name == user.display_name:
      await hook.send(arg,avatar_url=user.avatar_url)
      await hook.delete()
  await ctx.message.delete()

TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    client.run(TOKEN)
