from database_functions import *
from termcolor import cprint, colored
from encryption import *
import colorama

colorama.init()

cprint('Hello welcome to ManageMyPasswords [CLI Edition]', "green")
cprint('Created by Imira Randeniya', "yellow")
print('')

master_pswd = input('Enter master password for this password manager: ')
key = createKey(master_pswd)

print('')
create_tables()
insert_master_password(encryptString(key=key, str=master_pswd))
print('Finished now run main.py to start using the program.')
