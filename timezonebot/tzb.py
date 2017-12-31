import re

def timeString(hours,minutes,offset):
    hours = str((int(hours) + offset) % 24)
    minutes = str(minutes)
    while len(hours) < 2:
        hours = "0" + hours
    while len(minutes) < 2:
        minutes = "0" + minutes
    return hours + ":" + minutes

class Controller:
    def __init__(self):
        self.servers = []

    def getServerById(self,serverId):
        for s in self.servers:
            if s.serverId == serverId:
                return s
        return None

    def addServer(self,serverId):
        if self.getServerById(serverId) == None:
            self.servers.append(UserList(serverId))
        else:
            print("server already exists")

class User:
    def __init__(self,userId,name,timezone = 0):
        self.userId = userId
        self.timezone = 0
        self.name = name
        self.registered = False

    def setTimezone(self,timezone):
        self.timezone = timezone

    def setName(self,name):
        self.name = name

    def register(self):
        self.registered = True

class UserList:
    def __init__(self,serverId):
        self.users = []
        self.timezones = set()
        self.timezones.add(0)
        self.serverId = serverId

    def addUser(self,userId,name,timezone = None,r = False):
        if userId not in [u.userId for u in self.users]:
            print("adding new user " + userId + " " + name + str(timezone))
            newUser = User(userId,name)
            if r:
                newUser.register()
            if timezone != None:
                print("adding timezone for " + userId + " " + name + str(timezone))
                newUser.setTimezone(int(timezone))
                self.timezones.add(int(timezone))
            self.users.append(newUser)
        else:
            for u in self.users:
                if u.userId == userId and timezone != None and u.timezone != timezone:
                    print("updating timezone for " + userId + " " + name + str(timezone))
                    self.timezones.add(int(timezone))
                    print(self.timezones)
                    u.timezone = timezone
                    if r:
                        u.register()
        self.save()
        self.refreshTimezones()

    def getUserById(self,userId):
        for u in self.users:
            if u.userId == userId:
                return u
        return None

    def getTimezone(self,userId):
        for user in self.users:
            if user.userId == userId:
                return user.timezone
        print("user not found")
        return None

    def save(self):
        fname = "userlist" + self.serverId + ".txt"
        userlistStr = ""
        for user in self.users:
            userlistStr += user.userId + "," + user.name + "," + str(user.timezone) + "," + str(user.registered) + "\n"
        f = open(fname,"w")
        f.write(userlistStr)
        f.close()

    def load(self):
        fname = "userlist" + self.serverId + ".txt"
        print("loading from " + fname)
        try:
            f = open(fname,"r")
        except FileNotFoundError:
            f = open(fname,"w")
            f.close()
            f = open(fname,"r")
        userlistStr = f.read()
        f.close()
        userlistLst = userlistStr.split("\n")
        if len(userlistLst) > 1:
            for user in userlistLst:
                u = user.split(",")
                if len(u) > 1:
                    for data in u:
                        if u[3] == "True":
                            newr = True
                        else:
                            newr = False
                        self.addUser(u[0],u[1],timezone = int(u[2]),r = newr)
        print("done")
        

    def refreshTimezones(self):
        self.timezones = set()
        for u in self.users:
            self.timezones.add(u.timezone)

def parseTime(timestamp):
    hours = 0
    minutes = 0
    if re.match("^\d\d:\d\d$",timestamp):
        hours = int(timestamp[0:2])
        minutes = int(timestamp[3:5])
    elif re.match("^\d?\d:\d\d\W?am$",timestamp):
        hours = int(timestamp.split(":")[0])
        minutes = int(timestamp.split(":")[1][0:2])
        if hours == 12:
            hours = 0
    elif re.match("^\d?\d:\d\d\W?pm$",timestamp):
        hours = 12+int(timestamp.split(":")[0])
        minutes = int(timestamp.split(":")[1][0:2])
        if hours == 24:
            hours = 12
    elif re.match("^\d?\d\W?am$",timestamp):
        hours = int(timestamp.split("a")[0])
        if hours == 12:
            hours = 0
    elif re.match("^\d?\d\W?pm$",timestamp):
        hours = 12+int(timestamp.split("p")[0])
        if hours == 24:
            hours = 12
    elif re.match("^\d:\d\d$",timestamp):
        hours = int(timestamp.split(":")[0])
        minutes = int(timestamp.split(":")[1])
    else:
        print("cyan you fucked up")
    return [hours,minutes]

##testing-

##testdata = ["2137","21:37","9:37am","9:37pm","9am","9pm"]
##
##for testcase in testdata:
##    print(parseTime(testcase))
