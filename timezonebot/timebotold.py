import discord
from discord.ext import commands
import tzb
import re

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!tz_', description=description)

userlist = tzb.UserList()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("command prefix is " + bot.command_prefix)
    print('------')

users = {
    "160481323746590731":0,#cyan
    "208122604161204224":-8,#autumn
    "140324228745396225":-5,#bard
    "166068876008882176":-8,#of
    "196422115212132353":-5,#rory
    "190065758267637760":-8,#zoey
    "125424672765509632":-8,#tenttle
}
timezones = []
for u in users:
    if users[u] not in timezones:
        timezones.append(users[u])
timezones.sort()

@bot.event
async def on_message(message):
    if message.author != bot.user:
        print(message.content)
##        if re.match(bot.command_prefix + "register",message.content):
##            print("registering user...")
##            timezone = int(message.content.split(" ")[1])
##            if timezone > 0:
##                tzstring = "UTC+" + str(timezone)
##            elif timezone == 0:
##                tzstring = "UTC"
##            else:
##                tzstring = "UTC" + str(timezone)
##                
##            await bot.send_message(message.channel, "registered " + message.author.name + " in timezone UTC" + str(timezone))
##            userlist.addUser(message.author.id,message.author.name,timezone=timezone)

        timeMatches = re.findall("(\n|\W|^)(([01]\d|2[0-3]):([0-5]\d)|(([1-9]|1[0-2])(((:[0-5]\d)?\W?(pm|am))|(:[0-5]\d))))(\W|$|\n)",message.content)
        if len(timeMatches) > 0:
            reply = "```"
            for time in timeMatches:
                t = time[1]
                h = tzb.parseTime(t)[0]
                m = tzb.parseTime(t)[1]
            authorZone = 0
            if message.author.id in users:
                authorZone = users[message.author.id]
            for zone in timezones:
                mod = zone - authorZone
                newh = h+mod
                while newh >= 24:
                    newh -= 24
                while newh < 0:
                    newh += 24
                newm = m
                hours = str(newh)
                minutes = str(newm)
                if len(hours) == 1:
                    hours = "0" + hours
                if len(minutes) == 1:
                    minutes = "0" + minutes
                if zone > 0:
                    tzstring = "UTC+" + str(zone)
                elif zone == 0:
                    tzstring = "UTC  "
                else:
                    tzstring = "UTC" + str(zone)
                reply += tzstring + " - " + hours + ":" + minutes + "\n"
            reply += "```"
                
            await bot.send_message(message.channel, reply)
        

bot.run('MzkzNTgzNzI1NzAwNTc5MzQ1.DR35Dw.18TjXqYOYRpSoJsleb156WFu5mA')
