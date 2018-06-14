import js2py

CryptoJS = js2py.require('crypto-js')
JSON = js2py.eval_js('JSON')

key = "MYeo8OZvaQR2vqn4"

class Hasher:
    
    def encrypt(self, string):
        return CryptoJS.AES.encrypt(JSON.stringify(string), key)
    
    def decrypt(self, string):
        bytes = CryptoJS.AES.decrypt(string, key)
        decryptedString = bytes.toString(CryptoJS.enc.Utf8)
        return decryptedString
        
    def compareStrings(self, string1, string2):
        if self.decrypt(string1) == self.decrypt(string2):
            return True
        return False