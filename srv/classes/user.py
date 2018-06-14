from classes.auth import Auth
from classes.sql import SQL

auth = Auth('pukabooksrv')
sql = SQL()

class User:
    
    idUser = 0
    email = ""
    user = ""
    password = ""
    gUser = 0
    
    def __init__(self):
        authType = auth.getArraydcd()[0]
        if authType == 'Basic':
            dcdUser = auth.getUserPass64Decode(auth.getArraydcd())
            self.email = dcdUser[0]
            self.password = dcdUser[1]
        elif authType == 'Bearer':
            dcdUser = auth.getdcdToken(auth.getArraydcd())['data']
            self.email = dcdUser['email']
            self.password = dcdUser['password']
        extras = sql.getUser(unicode(self.email), unicode(self.password))
        self.idUser = extras['iduser']
        self.user = extras['user']
        self.gUser = extras['guser']
        