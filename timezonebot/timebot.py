import discord
import tzb
import re
import os

client = discord.Client()
command_prefix = "!!"
controller = tzb.Controller()

timezoneNames = {
    0:"UTC",
    -8:"PST",
    -5:"EST"
}

for filename in os.listdir("."):
    if filename.endswith(".txt") and filename.startswith("userlist"):
        serverId = filename.split("userlist")[1].split(".txt")[0]
        if len(serverId) > 10:
            controller.addServer(serverId)
            controller.servers[-1].load()

##users = {
##    "208122604161204224":-8,#autumn
##    "140324228745396225":-5,#bard
##    "166068876008882176":-8,#of
##    "196422115212132353":-5,#rory
##    "190065758267637760":-8,#zoey
##    "125424672765509632":-8,#tenttle
##}

##TODO:
##  -command to check what timezone a user is
##  -register a user's server(s) and only display their timezone in relevant servers
##  -fix timezone removal when no users are in the timezone

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
    if not message.channel.is_private:
        serverId = message.server.id
        print(serverId)
        messageServer = controller.getServerById(serverId)
        if messageServer == None:
            controller.addServer(serverId)
            messageServer = controller.getServerById(serverId)
        if message.content == command_prefix + "settimezone":
            await client.send_message(message.author,"what is your timezone offset from UTC? (eg. -8)")
            awaiting_response.add(message.author.id + "s" + message.server.id)
        if message.content.startswith(command_prefix + "timezone "):
            reply = "```"
            found = False
            for u in message.mentions:
                mentionedUser = messageServer.getUserById(u.id)
                if mentionedUser != None:
                    found = True
                    reply += u.name + ": "
                    if mentionedUser.timezone in timezoneNames:
                        reply += timezoneNames[mentionedUser.timezone]
                    elif mentionedUser.timezone > 0:
                        reply += "+" + str(mentionedUser.timezone)
                    elif mentionedUser.timezone < 0:
                        reply += str(mentionedUser.timezone)
                    reply += "\n"
                else:
                    reply += u.name + " not registered. " + u.mention + ", use !settimezone to set your timezone."
            reply += "```"
            if len(message.mentions) > 0:
                await client.send_message(message.channel,reply)

        for server in controller.servers:
            if message.server.id == server.serverId:
                server.addUser(message.author.id,message.author.name)

        if message.content == command_prefix + "manualsave":
            messageServer.save()
            print("done")

        if message.author != client.user:
            reply = ""
            authorZone = 0
            if authorZone == None:
                authorZone = 0
            for u in messageServer.users:
                if message.author.id == u.userId:
                    authorZone = int(u.timezone)
                    if not u.registered:
                        reply += "you have not registered. the following assumes you are in UTC. use !settimezone to register\n"
            reply += "```"
            messageStr = message.content.lower()
            timeMatches = re.findall("(\n|\W|^)(([01]\d|2[0-3]):([0-5]\d)|(([1-9]|1[0-2])(((:[0-5]\d)?\W?(pm|am))|(:[0-5]\d))))(\W|$|\n)",messageStr)
            if message.content == command_prefix + "timenow":
                currentHours = int(message.timestamp.hour) #get hour message was sent
                currentHours += authorZone #add the timezone of the message author
                currentHours = currentHours%24 #set it within a 24-hour range
                currentHours = str(currentHours) #convert to string
                currentMinutes = str(message.timestamp.minute) #get minute message was sent
                while len(currentHours) < 2:
                    currentHours = "0" + currentHours #make hours 2-digit
                while len(currentMinutes) < 2: 
                    currentMinutes = "0" + currentMinutes #make minutes 2-digit
                timeMatches = [["",currentHours + ":" + currentMinutes]] #use a shitty format that i havent fixed yet
            if len(timeMatches) > 0:
                for time in timeMatches:
                    t = time[1]
                    h = tzb.parseTime(t)[0]
                    m = tzb.parseTime(t)[1]
                for zone in sorted(messageServer.timezones):
                    zone = int(zone)
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
                        
                    if zone in timezoneNames:
                        tzstring = timezoneNames[zone] + "  "
                    elif zone > 0:
                        tzstring = "UTC+" + str(zone)
                    elif zone == 0:
                        tzstring = "UTC  "
                    else:
                        tzstring = "UTC" + str(zone)
                        
                    reply += tzstring + " - " + hours + ":" + minutes + "\n"
                reply += "```"
                    
                await client.send_message(message.channel, reply)

    else:
        marked_for_removal = []
        for user in awaiting_response:
            if user.split("s")[0] == message.author.id:
                authorId = message.author.id
                serverId = user.split("s")[1]
                messageServer = controller.getServerById(serverId)
                try:
                    newtimezone = int(message.content)
                    if -12 < newtimezone <= 12:
                        messageServer.addUser(message.author.id,message.author.name,newtimezone)
                        messageServer.getUserById(message.author.id).register()
                        await client.send_message(message.author,"your timezone has been set to UTC" + ("+" if newtimezone>=0 else "") + str(newtimezone))
                        marked_for_removal.append(message.author.id + "s" + serverId)
                    else:
                        await client.send_message(message.author,"please enter a valid offset from UTC (between -12 and 12)")
                except ValueError:
                    await client.send_message(message.author,"please enter a valid offset from UTC (between -12 and 12)")
        for u in marked_for_removal:
            awaiting_response.remove(u)
        

client.run('MzkzNTgzNzI1NzAwNTc5MzQ1.DR35Dw.18TjXqYOYRpSoJsleb156WFu5mA')
