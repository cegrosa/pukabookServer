from flask import jsonify, request
from sql import SQL
import jwt, string, base64, time

class Auth:
    
    secretKey = ''
    sql = SQL()
    
    def __init__(self, secretKey):
        self.secretKey = secretKey
        
    def getArraydcd(self):
        headers = request.headers["Authorization"]
        dcdArray = string.split(headers, ' ')
        return dcdArray
        
    def getdcdToken(self, dcdArray):
        return jwt.decode(dcdArray[1], self.secretKey, algorithm='HS256')
        
    def getUserPass64Decode(self, dcdArray):
        userPass = base64.b64decode(dcdArray[1])
        return string.split(userPass, ':')
        
    def checkData(self):
        dcdArray = self.getArraydcd()
        
        if len(dcdArray) == 2:
            if dcdArray[0] == 'Basic':
                return self.isBasic(dcdArray)
            elif dcdArray[0] == 'Bearer':
                return self.isBearer(dcdArray)
                
    def isBasic(self, dcdArray):
        dcdUser = self.getUserPass64Decode(dcdArray)
        if len(dcdUser) == 2:
            if self.sql.checkUser(dcdUser[0], dcdUser[1]):
                return self.signIn({
                    'email' : dcdUser[0],
                    'password' : dcdUser[1],
                })
        return {
            "auth" : False,
            "t" : None
        }
                
    def isBearer(self, dcdArray):
        dcdToken = self.getdcdToken(dcdArray)
        localTime = time.time()
        
        if localTime < dcdToken["expire"]:
            tokenBody = {
                "expire" : localTime + (60*60),
                "data" : dcdToken["data"]
            }
            
            return {
                "auth" : True,
                "t" : jwt.encode(tokenBody, self.secretKey, algorithm='HS256')
            }
        return {
            "auth" : False,
            "t" : None
        }
    
        
    def signIn(self, data):
        localTime = time.time()
        
        token = {
            "expire" : localTime + (60*60),
            "data" : data,
        }
        
        return {
            "auth" : True,
            "t" : jwt.encode(token, self.secretKey, algorithm='HS256'),
        }
        
        