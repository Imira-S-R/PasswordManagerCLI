from cryptography.fernet import Fernet,InvalidToken
import hashlib
import base64
from prompt_toolkit import prompt

def askPassphrase(str):
    
    passphrase=prompt(str, is_password=True)
    if passphrase=="":
        return None
    key=createKey(passphrase)
    #passphrase=hashlib.sha256(passphrase.encode('utf-8')).digest()
    #passphrase=base64.urlsafe_b64encode(passphrase)
    return key

def createKey(str):
    key=hashlib.sha256(str.encode('utf-8')).digest()
    key=base64.urlsafe_b64encode(key)
    return key

def encryptString(key,str):
    if str==None or str=="":
        return
    fernet = Fernet(key)
    encryptedString = fernet.encrypt(str.encode("utf-8"))
    return encryptedString.decode("utf-8")

def decryptString(key,str):
    if str==None or str=="":
        return
    fernet = Fernet(key)
    decryptedString = fernet.decrypt(str.encode("utf-8"))
    return decryptedString.decode("utf-8")

# key = askPassphrase('enter: ')
# print(key)
# print(encryptString(key, 'hello'))
# # print(decryptString())