import discord
import keep_alive
client=discord.Client()
@client.event
async def on_message(msg):
  if not "--" in msg.content:
    return
  if msg.content=="":
    return
  if not msg.author.id==client.user.id:
    return
  try:
    embed=discord.Embed(description=msg.content,color=444444)
    await msg.channel.send(embed=embed)
    await msg.delete()
  except:
    pass
keep_alive.keep_alive()
client.run("Njc0MTcyMTA5OTkxMzEzNDEy.X2CvFg.F1bthpil29sfU3I5GdCx6IL4vfw",bot=False)
