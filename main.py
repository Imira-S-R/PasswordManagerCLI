from database_functions import *
import os
from termcolor import cprint, colored
import colorama
import subprocess
import getpass
from encryption import *
import argparse


colorama.init()

menu = '''
1. Add New Password
2. Edit Password
3. Delete Password
4. View Passwords
5. Find a password for a site or app
6. Find the websites/apps connected to an e-mail/username
7. Exit
'''

clear = lambda: os.system('cls')

parser = argparse.ArgumentParser()

parser.add_argument('--name', '-n', type=str, help="website/app name", default='no')
parser.add_argument('--username', '-u', type=str, help="username", default='no')
parser.add_argument('--password', '-p', type=str, help="password", default='no')
args = parser.parse_args()

if args.name != 'no' and args.username != 'no' and args.password != 'no':
    key = askPassphrase('Enter master password: ')

    website_name = encryptString(key, args.name)
    username = encryptString(key, args.username)
    password = encryptString(key, args.password)

    insert_password(website_name=website_name, username=username, password=password)
    cprint('Password Inserted.', "green")
    exit()


def authenticate ():
    master_pswd = get_master_pswd()

    print('')
    password = getpass.getpass(prompt='Enter Master Password: ')
   
    if master_pswd[0][1] == password:
        clear()
        print('The Master Password Is Correct. Welcome back')
    else:
        print('The password is wrong')
        exit()
       

def search (website_name):
    key = askPassphrase('Enter master password: ')
    filteredList = get_specific_records(key, website_name=website_name)
    return filteredList

def addPassword():

    print('Enter website name: ')
    website_name = input('> ')
    print('')
    print('Enter username: ')
    username = input('> ')
    print('')
    print('Enter password: ')
    password = input('> ')
    print('')

    key = askPassphrase('Enter master password: ')
    # createKey(key)

    website_name = encryptString(key, website_name)
    username = encryptString(key, username)
    password = encryptString(key, password)

    insert_password(website_name=website_name, username=username, password=password)
    print('')
    cprint('Password Inserted.', "green")

    # clear()
    main()

def editPassword():

    id = int(input('Enter id of the password you want to change: '))

    passwords = get_specific_info(id)
    key = askPassphrase('Enter master password: ')

    print('')
    cprint(f'RESULT FOR ID {id}', "red")
    print(f'Name: {decryptString(key, passwords[0][1])}')
    print(f'Username: {decryptString(key, passwords[0][2])}')
    print(f'Password: {decryptString(key, passwords[0][3])}')
    cprint('-' * 30, "red")

    print('')
    cprint('Enter SAB for the same entry as before.', "red")
    print('')

    print('Enter website name: ')
    website = input('> ')
    print('')
    print(f'Enter username for {website}: ')
    username = input('> ')
    print('')
    print(f'Enter password: for {website}')
    password = input('> ')
    print('')

    if website == 'SAB':
        website = decryptString(key, passwords[0][1])
    else:
        website = website
    if username == 'SAB':
        username = decryptString(key, passwords[0][2])
    else:
        username = username
    if password == 'SAB':
        password = decryptString(key, passwords[0][3])
    else:
        password = password

    update_passwords(password_id=id, website_name=encryptString(key, website), username=encryptString(key, username), password=encryptString(key, password))

    clear()
    main()

def deletePassword():

    id = int(input('Enter id of the password you want to delete: '))

    delete_password(password_id=id)

    clear()
    main()

def viewPasswords():
    passwords = get_records()

    key = askPassphrase('Enter master password: ')
    
    clear()

    for password in passwords:
        print('\n')
        cprint('-' * 20, "red")
        print('ID: ', password[0])
        print('Website Name: ', decryptString(key, password[1]))
        print('Username: ', decryptString(key, password[2]))
        print('Password: ', decryptString(key, password[3]))
        cprint('-' * 20, "red")

    main()

cprint('Hello welcome to ManageMyPasswords [CLI Edition]', "green")
cprint('Created by Imira Randeniya', "yellow")
authenticate()


def main ():

    print(menu)
    option = int(input('Enter option number: '))

    if option == 1:
        clear()
        addPassword()
    elif option == 2:
        clear()
        editPassword()
    elif option == 3:
        clear()
        deletePassword()
    elif option == 4:
        viewPasswords()
    elif option == 5:
        clear()
        website_name = input('Enter website name: ')
        key = askPassphrase('Enter master password: ')
        get_specific_records(key, website_name)
        main()
    elif option == 6:
        clear()
        print('Enter e-mail/username you want to find connected apps for: ')
        email = input('> ')
        print('')
        key = askPassphrase('Enter master password: ')
        get_email_connected_apps(key, email)
        main()
    elif option == 7:
        cprint('Program Finished', "red")
        exit()
    else:
        print('Invalid Option')

main()