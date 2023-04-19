import discord
from discord.ext import commands
import nationstates as ns
import asyncio
import unix

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='t ', intents=intents)
api = ns.Nationstates(user_agent="TEAL tool, recruitment script used through a discord bot. Created by: Jyezet")
bot.remove_command('help')
recruiter = None # The person who will be able to use the recruiting commands at a time
recruiterName = None
motivation = True
rawTemplate = None
time = None

@bot.command(aliases=["r", "recruit"])
async def Recruit(ctx):
  global recruiter
  global recruiterName
  global motivation
  global rawTemplate
  global time

  if ctx.author.id == recruiter:
    ETA = int(unix.gettime()) + int(time) # Current UNIX timestamp + waiting time = UNIX timestamp for when the bot sends the batch
    embed = discord.Embed(title="Recruitment running", description=f"Current recruiter: {recruiterName}", color=0x008080)
    embed.add_field(name="", value=f"Scanning for new nations, please wait {time} seconds. \nETA: <t:{ETA+1}:R>", inline=False)
    if motivation: # Add motivational quote in case they are enabled
      embed.add_field(name="", value="```\"If you want to go fast, go alone. \nIf you want to go far, go together.\" \n-African proverb```")
    embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    embed.set_footer(text="Made by Jyezet, Qekitor and Destiny")
    msg = await ctx.send(embed=embed)

    editedEmbed = discord.Embed(title="Recruitment running", description=f"Current recruiter: {recruiterName}", color=0x008080)
    editedEmbed.add_field(name="", value=f"Scanning for new nations, please wait {time} seconds. \n**New round of batches has been sent.**", inline=False)
    if motivation: # Add motivational quote in case they are enabled
      editedEmbed.add_field(name="", value="```\"If you want to go fast, go alone. \nIf you want to go far, go together.\" \n-African proverb```")
    editedEmbed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    editedEmbed.set_footer(text="Made by Jyezet, Qekitor and Destiny")

    editedEmbed2 = discord.Embed(title="Recruitment running", description=f"Current recruiter: {recruiterName}", color=0x008080)
    editedEmbed2.add_field(name="", value=f"Scanning for new nations, please wait {time} seconds. \n**No new nations have been created.**", inline=False)
    if motivation: # Add motivational quote in case they are enabled
      editedEmbed2.add_field(name="", value="```\"If you want to go fast, go alone. \nIf you want to go far, go together.\" \n-African proverb```")
    editedEmbed2.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    editedEmbed2.set_footer(text="Made by Jyezet, Qekitor and Destiny")

    # Get new nations shard
    newnations1 = (api.world().get_shards("newnations")["newnations"]).split(",")
    await asyncio.sleep(time) # Wait the assigned time before scanning for a batch,
    # it's a time.sleep instead of an asyncio.sleep because in this case, the bot must get locked in order not to skip the time.
    
    # From %TEMPLATE-ID% to %25TEMPLATE-ID%25 (That way the browser can read it)
    rawTemplate2 = rawTemplate.replace("%", "")
    template = f"%25{rawTemplate2}%25"
    
    # Get new nations shard again to compare differences (newly created nations within the recruiting process)
    newnations2 = (api.world().get_shards("newnations")["newnations"]).split(",")
    newnations = list(set(newnations2) - set(newnations1))
    while True:
      newnations2 = (api.world().get_shards("newnations")["newnations"]).split(",")
      newnations = list(set(newnations2) - set(newnations1))
      if not newnations: # If there are not new nations, stop the command
        embed = discord.Embed(title="TEAL", description=f"Current recruiter: {recruiterName}", color=0xfc0320)
        embed.add_field(name="", value="No new nations, scanning again.", inline=False)
        embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
        embed.set_footer(text="Made by Jyezet, Qekitor and Destiny")
        await ctx.send(embed=embed)
        await msg.edit(embed=editedEmbed2)
        await asyncio.sleep(30)
      else:
        break
    sendTo1Raw = []
    sendTo2Raw = []
    links = []

    for x in newnations:
      if len(sendTo1Raw) <= 8:
        sendTo1Raw.append(x)
      elif len(senTo2Raw) <= 16:
        sendTo2Raw.append(x)
      else:
        break
    sendTo1 = ",".join(sendTo1Raw) # Delete brackets, extra whitespaces and extra commas in one go. For the record, this line used to use like 8 nested .replace methods
    sendTo2 = ",".join(sendTo2Raw)

    if not sendTo2: # If there's no second batch just send the first one
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo1}&message={template}")
    else:
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo1}&message={template}")
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo2}&message={template}")

    # Turn the raw links into a nice embedded message
    embed = discord.Embed(title="Recruitment running", description=f"Current recruiter: {recruiterName}", color=0x008080)
    embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    embed.set_footer(text="Made by Jyezet, Qekitor and Destiny")
    for x in range(len(links)):
        embed.add_field(name="", value=f"[Batch number {x+1}]({links[x]})", inline=False)
    embed.add_field(name="", value="Once you send all TGs, use t recruit", inline=False)
    await ctx.send(ctx.message.author.mention, embed=embed) # Send the embedded message
    await msg.edit(embed=editedEmbed)
  else:
    embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320)
    embed.add_field(name="", value="You are not the assigned recruiter", inline=False)
    embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    embed.set_footer(text="Made by Jyezet, Qekitor and Destiny")
    await ctx.send(embed=embed) # Only the one who uses .s can use the recruitment commands

@bot.event 
async def on_command_error(ctx, error): # What happens when someone inputs a non-existant command
  if isinstance(error, commands.CommandNotFound): 
    embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320) 
    embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    embed.add_field(name="", value="Command not found.\nUse t rhelp to see the full commands list.", inline=False)
    embed.set_footer(text="Made by Jyezet, Qekitor and Destiny")
    await ctx.send(embed=embed)

@bot.command(aliases=["rh"])
async def help(ctx):
  embed = discord.Embed(title="Recruitment help", description="Note: Discord commands are case-sensitive", color=0x008080)
  embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png") 
  embed.add_field(name="rhelp (rh)", value="```Show this help section.```", inline=False)
  embed.add_field(name="toggleMotivation (tm|togglemotivation|togglemotivationalquotes)", value="```Toggle on or off motivational quotes.```", inline=False)
  embed.add_field(name="setRecruiter (s|setrecruiter) [Template-id] [Scanning time in seconds]", value="```Input all the information the bot needs to start recruiting.```", inline=False)
  embed.add_field(name="Recruit (r|recruit)", value="```Wait an inputted amount of time before sending batch(es).```", inline=False)
  embed.add_field(name="Finish (f|finish)", value="```Finish the current recruiting session, leaving the bot free for anyone to use.```", inline=False)
  await ctx.send(embed=embed)

@bot.command(aliases=["tm", "togglemotivation", "togglemotivationalquotes"])
async def toggleMotivation(ctx):
  try:
    global recruiter
    global motivation
    if ctx.author.id == recruiter:
      if motivation == False:
        motivation = True
        embed = discord.Embed(title="Recruitment settings", description=f"Current recruiter: {recruiterName}", color=0x11ff00)
        embed.add_field(name="", value="Motivational quotes have been enabled", inline=False)
        embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
        embed.set_footer(text="Made by Jyezet, Qekitor and Destiny")
        await ctx.send(embed=embed)
      else:
        motivation = False
        embed = discord.Embed(title="Recruitment settings", description=f"Current recruiter: {recruiterName}", color=0x0044ff)
        embed.add_field(name="", value="Motivational quotes have been disabled", inline=False)
        embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
        embed.set_footer(text="Made by Jyezet, Qekitor and Destiny")
        await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320)
      embed.add_field(name="", value="You are not the assigned recruiter", inline=False)
      embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
      embed.set_footer(text="Made by Jyezet, Qekitor and Destiny")
      await ctx.send(embed=embed) # Only the one who uses t s can use the recruitment commands
  except:
    embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320) 
    embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    embed.add_field(name="", value="Invalid syntax.\nUse t rhelp to see the full commands list.", inline=False)
    embed.set_footer(text="Made by Jyezet, Qekitor and Destiny")
    await ctx.send(embed=embed)

@bot.command(aliases=["s", "setrecruiter"])
async def setRecruiter(ctx, localRawTemplate: str, localTime: float):
  try:
    global recruiter
    global recruiterName
    global motivation
    global rawTemplate
    global time

    if localTime < 30:
      embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320) 
      embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
      embed.add_field(name="", value="Wait time can't be lower than 30 seconds", inline=False)
      embed.set_footer(text="Made by Jyezet, Qekitor and Destiny")
      await ctx.send(embed=embed)
      return

    rawTemplate = localRawTemplate
    time = localTime

    recruiter = ctx.author.id
    recruiterName = ctx.author
    embed = discord.Embed(title="Recruitment settings", description=f"Current recruiter: {recruiterName}", color=0x008080)
    
    if motivation: # Add motivational quote in case they are enabled
      embed.add_field(name="", value="```\"The journey of a thousand\n miles begins with one step.\" \n-Lao Tzu```", inline=False)
    embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    embed.set_footer(text="Made by Jyezet, Qekitor and Destiny")
    await ctx.send(embed=embed)
  except:
    embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320) 
    embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    embed.add_field(name="", value="Invalid syntax.\nUse t rhelp to see the full commands list.", inline=False)
    embed.set_footer(text="Made by Jyezet, Qekitor and Destiny")
    await ctx.send(embed=embed)

@bot.command(aliases=["f", "finish"])
async def Finish(ctx):
  try:
    global recruiter
    global recruiterName
    global motivation
    if recruiter != None and recruiterName != None: # Only finish recruiting if someone has already started recruiting
      if ctx.author.id == recruiter:
        recruiter = None
        recruiterName = None

        embed = discord.Embed(title="Recruitment settings", description=f"Current recruiter: None", color=0x008080)
        if motivation: # Add motivational quote in case they are enabled
          embed.add_field(name="", value="```\"Even if you’re on\n the right track, you’ll\n get run over if you just\n sit there.\" -Will Rogers```", inline=False)
        embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
        embed.set_footer(text="Made by Jyezet, Qekitor and Destiny")
        await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320)
      embed.add_field(name="", value="You are not the assigned recruiter", inline=False)
      embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
      embed.set_footer(text="Made by Jyezet, Qekitor and Destiny")
      await ctx.send(embed=embed) # Only the one who uses t s can use the recruitment commands
  except:
    embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320) 
    embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    embed.add_field(name="", value="Invalid syntax.\nUse t rhelp to see the full commands list.", inline=False)
    embed.set_footer(text="Made by Jyezet, Qekitor and Destiny")
    await ctx.send(embed=embed)

bot.run("MTA4OTcwNjM5NTgxOTA2MTI3OA.GkRYu6.iNKWzpGXAgB_uf0E1f2OwVRsDD6kIDm1_i5fSc") # INSERT YOUR BOT TOKEN BETWEEN THE QUOTES