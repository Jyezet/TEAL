import discord
from discord.ext import commands
import nationstates as ns
import asyncio
import random as rn
import unix

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='t ', intents=intents)
useragent = input("Insert your nation name:")
api = ns.Nationstates(user_agent=useragent)
bot.remove_command('help')
recruiter = None # The person who will be able to use the recruiting commands at a time
recruiterName = None
motivation = True
motivational_quotes = ["```\"If you want to go fast, go alone. If you want to go far, go together.\" -African proverb```",
                       "```\"Even if you\'re on the right track, you\'ll get run over if you just sit there.\" -Will Rogers```",
                       "```\"The journey of a thousand miles begins with one step.\" -Lao Tzu```",
                       "```\"Learn as if you will live forever, live like you will die tomorrow.\" — Mahatma Gandhi```",
                       "```\"The pessimist sees difficulty in every opportunity. The optimist sees opportunity in every difficulty.\" — Winston Churchill```",
                       ]
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
    ETA = int(unix.gettime()) + time # Current UNIX timestamp + waiting time = UNIX timestamp for when the bot sends the batch
    embed = discord.Embed(title="Recruitment running", description=f"Current recruiter: {recruiterName}", color=0x008080)
    embed.add_field(name="", value=f"Scanning for new nations, please wait {time} seconds. \nETA: <t:{ETA+1}:R>", inline=False)
    if motivation: # Add motivational quote in case they are enabled
      quote = rn.randint(0, len(motivational_quotes))
      embed.add_field(name="", value=motivational_quotes[quote], inline=False)
    embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
    msg = await ctx.send(embed=embed)
    editedEmbed = discord.Embed(title="Recruitment running", description=f"Current recruiter: {recruiterName}", color=0x008080)
    editedEmbed.add_field(name="", value=f"Scanning for new nations, please wait {time} seconds. \n**New round of batches has been sent.**", inline=False)
    if motivation: # Add motivational quote in case they are enabled
      quote = rn.randint(0, len(motivational_quotes))
      editedEmbed.add_field(name="", value=motivational_quotes[quote], inline=False)
    editedEmbed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    editedEmbed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")

    editedEmbed2 = discord.Embed(title="Recruitment running", description=f"Current recruiter: {recruiterName}", color=0x008080)
    editedEmbed2.add_field(name="", value=f"Scanning for new nations, please wait {time} seconds. \n**No new nations have been created.**", inline=False)
    if motivation: # Add motivational quote in case they are enabled
      quote = rn.randint(0, len(motivational_quotes))
      editedEmbed2.add_field(name="", value=motivational_quotes[quote], inline=False)
    editedEmbed2.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    editedEmbed2.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")

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
        embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
        await ctx.send(embed=embed)
        await msg.edit(embed=editedEmbed2)
        await asyncio.sleep(time)
      else:
        break
    sendTo1Raw = []
    sendTo2Raw = []
    sendTo3Raw = []
    sendTo4Raw = []
    sendTo5Raw = []
    links = []

    for x in newnations:
      if len(sendTo1Raw) <= 7:
        sendTo1Raw.append(x)
      elif len(sendTo2Raw) <= 7:
        sendTo2Raw.append(x)
      elif len(sendTo3Raw) <= 7:
        sendTo3Raw.append(x)
      elif len(sendTo4Raw) <= 7:
        sendTo4Raw.append(x)
      elif len(sendTo5Raw) <= 7:
        sendTo5Raw.append(x)
      else:
        break
    sendTo1 = ",".join(sendTo1Raw) # Delete brackets, extra whitespaces and extra commas in one go. For the record, this line used to use like 8 nested .replace methods
    sendTo2 = ",".join(sendTo2Raw)
    sendTo3 = ",".join(sendTo3Raw)
    sendTo4 = ",".join(sendTo4Raw)
    sendTo5 = ",".join(sendTo5Raw)

    if not sendTo2: # This yandere ah code is to check what variables are not empty and thus can be put in a batch
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo1}&message={template}")
    elif not sendTo3:
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo1}&message={template}")
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo2}&message={template}")
    elif not sendTo4:
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo1}&message={template}")
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo2}&message={template}")
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo3}&message={template}")
    elif not sendTo5:
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo1}&message={template}")
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo2}&message={template}")
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo3}&message={template}")
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo4}&message={template}")
    else:
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo1}&message={template}")
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo2}&message={template}")
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo3}&message={template}")
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo4}&message={template}")
      links.append(f"https://www.nationstates.net/page=compose_telegram?tgto={sendTo5}&message={template}")

      # Turn the raw links into a nice embedded message
      embed = discord.Embed(title="Recruitment running", description=f"Current recruiter: {recruiterName}", color=0x008080)
      embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
      embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
      for x in range(len(links)):
          embed.add_field(name="", value=f"[Batch number {x+1}]({links[x]})", inline=False)
      embed.add_field(name="", value="Once you send all TGs, use t recruit", inline=False)
      await ctx.send(ctx.message.author.mention, embed=embed) # Send the embedded message
      await msg.edit(embed=editedEmbed)
  else:
    embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320)
    embed.add_field(name="", value="You are not the assigned recruiter", inline=False)
    embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
    await ctx.send(embed=embed) # Only the one who uses t s can use the recruitment commands

@bot.event 
async def on_command_error(ctx, error): # What happens when someone inputs a non-existant command
  if isinstance(error, commands.CommandNotFound): 
    embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320) 
    embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    embed.add_field(name="", value="Command not found.\nUse t help to see the full commands list.", inline=False)
    embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
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
        embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
        await ctx.send(embed=embed)
      else:
        motivation = False
        embed = discord.Embed(title="Recruitment settings", description=f"Current recruiter: {recruiterName}", color=0x0044ff)
        embed.add_field(name="", value="Motivational quotes have been disabled", inline=False)
        embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
        embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
        await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320)
      embed.add_field(name="", value="You are not the assigned recruiter", inline=False)
      embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
      embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
      await ctx.send(embed=embed) # Only the one who uses t s can use the recruitment commands
  except:
    embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320) 
    embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    embed.add_field(name="", value="Invalid syntax.\nUse t help to see the full commands list.", inline=False)
    embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
    await ctx.send(embed=embed)

@bot.command(aliases=["s", "setrecruiter"])
async def setRecruiter(ctx, localRawTemplate: str, localTime: int):
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
      embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
      await ctx.send(embed=embed)
      return
    if recruiter == None or recruiter == ctx.author.id:
      rawTemplate = localRawTemplate
      time = localTime
      recruiter = ctx.author.id
      recruiterName = ctx.author
      embed = discord.Embed(title="Recruitment settings", description=f"Current recruiter: {recruiterName}", color=0x008080)
      if motivation: # Add motivational quote in case they are enabled
        quote = rn.randint(0, len(motivational_quotes))
        embed.add_field(name="", value=motivational_quotes[quote], inline=False)
      embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
      embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320)
      embed.add_field(name="", value="You are not the assigned recruiter", inline=False)
      embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
      embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
      await ctx.send(embed=embed) # Only the one who uses t s can use the recruitment commands
  except:
    embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320) 
    embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    embed.add_field(name="", value="Invalid syntax.\nUse t help to see the full commands list.", inline=False)
    embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
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
          quote = rn.randint(0, len(motivational_quotes))
          embed.add_field(name="", value=motivational_quotes[quote], inline=False)
        embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
        embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
        await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320)
      embed.add_field(name="", value="You are not the assigned recruiter", inline=False)
      embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
      embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
      await ctx.send(embed=embed) # Only the one who uses t s can use the recruitment commands
  except:
    embed = discord.Embed(title="Error", description=f"Current recruiter: {recruiterName}", color=0xfc0320) 
    embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png")
    embed.add_field(name="", value="Invalid syntax.\nUse t help to see the full commands list.", inline=False)
    embed.set_footer(text=f"Made by Jyezet, Qekitor and Destiny, and run by: {useragent}")
    await ctx.send(embed=embed)

@bot.command(aliases=["h"])
async def help(ctx):
  embed = discord.Embed(title="Recruitment help", description="Note: Discord commands are case-sensitive", color=0x008080)
  embed.set_author(name="TEAL", icon_url="https://i.imgur.com/oPZTgUN.png") 
  embed.add_field(name="help (h)", value="```Show this help section.```", inline=False)
  embed.add_field(name="toggleMotivation (tm|togglemotivation|togglemotivationalquotes)", value="```Toggle on or off motivational quotes.```", inline=False)
  embed.add_field(name="setRecruiter (s|setrecruiter) [Template-id] [Scanning time in seconds]", value="```Input all the information the bot needs to start recruiting.```", inline=False)
  embed.add_field(name="Recruit (r|recruit)", value="```Wait an inputted amount of time before sending batch(es).```", inline=False)
  embed.add_field(name="Finish (f|finish)", value="```Finish the current recruiting session, leaving the bot free for anyone to use.```", inline=False)
  await ctx.send(embed=embed)

bot.run("MTA4OTcwNjM5NTgxOTA2MTI3OA.GXMWzh.ZDd5hE_A98Wvv-yBKykw_ed68g8DPpT3igtoZM") # INSERT YOUR BOT TOKEN BETWEEN THE QUOTES