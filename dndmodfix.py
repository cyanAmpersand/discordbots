import discord
from discord.ext import commands
import random
import re

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    maxrolls = 10
    maxsides = 120
    minmod = -5
    maxmod = 10
    adv = 0
    if dice[-1] == "a":
        adv = 1
        dice = dice[:-1]
    elif dice[-1] == "d":
        adv = -1
        dice = dice[:-1]
    try:
        rolls, limit, modifier = map(int, re.split('d|m',dice))
    except Exception:
        try:
            rolls, limit = map(int, re.split('d',dice))
            modifier = 0
        except Exception:
            await bot.say('Format must be NdN or NdNmX')
            return

    if rolls < 1 or limit < 1:
        await bot.say('Cannot roll negative dice')
        return
    results = []
    results2 = []
    s_results = []
    total = 0
    for r in range(rolls):
        newroll = random.randint(1,limit)
        newroll2 = random.randint(1,limit)
        results.append(newroll)
        results2.append(newroll2)
    for r in range(len(results)):
        if adv > 0:
            if results[r] > results2[r]:
                total += results[r]
                s_results.append("**"+str(results[r])+"**|"+str(results2[r]))
            else:
                total += results2[r]
                s_results.append(str(results[r])+"|**"+str(results2[r])+"**")
        elif adv < 0:
            if results[r] < results2[r]:
                total += results[r]
                s_results.append("**"+str(results[r])+"**|"+str(results2[r]))
            else:
                total += results2[r]
                s_results.append(str(results[r])+"|**"+str(results2[r])+"**")
        else:
            total += results[r]
            s_results.append(str(results[r]))
            
    if limit > maxsides:
        await bot.say('Exceeds maximum number of sides')
        return
    if rolls > maxrolls:
        await bot.say('Exceeds maximum number of rolls')
        return
    if modifier < minmod or modifier > maxmod:
        await bot.say('Modifier out of range')
        return
    
    result = ' + '.join(s_results)
    if modifier != 0:
        result += ' + ' + str(modifier) + ' (mod)'
        total += modifier
    if rolls > 1 or modifier != 0:
        result += ' = ' + str(total)
        
    await bot.say(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

bot.run('MzY0MDU1NjE3NDQwMDU1Mjk2.DLKMvA.NsO5u15ZUKRA3TiHSo0uOKkWhLw')
