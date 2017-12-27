import discord
import tzb
import re

client = discord.Client()

userlist = tzb.UserList()
userlist.load()

##users = {
##    "208122604161204224":-8,#autumn
##    "140324228745396225":-5,#bard
##    "166068876008882176":-8,#of
##    "196422115212132353":-5,#rory
##    "190065758267637760":-8,#zoey
##    "125424672765509632":-8,#tenttle
##}

awaiting_response = set()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    print(message.content)
    if message.content == "!register":
        await client.send_message(message.author,"what is your timezone offset from UTC? (eg. -8)")
        awaiting_response.add(message.author.id)

    userlist.addUser(message.author.id,message.author.name)

    if message.content == "!manualsave":
        userlist.save()
        print("done")

    if message.channel.is_private:
        if message.author.id in awaiting_response:
            try:
                newtimezone = int(message.content)
                if -12 < newtimezone <= 12:
                    userlist.addUser(message.author.id,message.author.name,newtimezone)
                    userlist.getUserById(message.author.id).register()
                    await client.send_message(message.author,"your timezone has been set to UTC" + ("+" if newtimezone>=0 else "") + str(newtimezone))
                    awaiting_response.remove(message.author.id)
                else:
                    await client.send_message(message.author,"please enter a valid offset from UTC (between -12 and 12)")
            except ValueError:
                await client.send_message(message.author,"please enter a valid offset from UTC (between -12 and 12)")

    if message.author != client.user:
        messageStr = message.content.lower()
        timeMatches = re.findall("(\n|\W|^)(([01]\d|2[0-3]):([0-5]\d)|(([1-9]|1[0-2])(((:[0-5]\d)?\W?(pm|am))|(:[0-5]\d))))(\W|$|\n)",messageStr)
        if len(timeMatches) > 0:
            reply = ""
            for time in timeMatches:
                t = time[1]
                h = tzb.parseTime(t)[0]
                m = tzb.parseTime(t)[1]
            authorZone = 0
            if authorZone == None:
                authorZone = 0
            for u in userlist.users:
                if message.author.id == u.userId:
                    authorZone = u.timezone
                    if not u.registered:
                        reply += "you have not registered. the following assumes you are in UTC. use !register to register\n"
            reply += "```"
            for zone in sorted(userlist.timezones):
                zone = int(zone)
                authorZone = int(authorZone)
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
                
            await client.send_message(message.channel, reply)
        

client.run('MzkzNTgzNzI1NzAwNTc5MzQ1.DR35Dw.18TjXqYOYRpSoJsleb156WFu5mA')
