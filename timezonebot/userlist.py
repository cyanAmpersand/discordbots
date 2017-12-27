class User:
    def __init__(self,userId):
        self.userId = userId
        self.timezone = 0

    def setTimezone(self,timezone):
        self.timezone = timezone

class UserList:
    def __init__(self):
        self.users = []

    def addUser(self,userId,timezone):
        newUser = User(userId)
        newUser.setTimezone(timezone)
        self.users.append(newUser)

    def getTimezone(self,userId):
        for user in self.users:
            if user.userId == userId:
                return user.timezone
        print("user not found")
        return None

userlist01 = UserList()
userlist01.addUser("160481323746590731",0)
