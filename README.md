# ManageMyPasswords (CLI Edition)
A CLI Password Manager made using Python and Postgresql database.

## Quick Start Guide
First Clone The Project
```js

git clone https://github.com/Imira-S-R/PasswordManagerCLI

```
Change The Direcory
```js

cd PasswordManagerCLI

```
Install Python Packages
```js

pip install -r requirements.txt

```
Run setup.py for first time users
```js

python setup.py

```
After that run main.py
```js

python main.py

```
Create a table in postgresql
```js

CREATE DATABASE passwords;

```
## Shortcut Commands
To Add A Password
```js

python main.py -n "name" -u "username" -p "password"

```
List The Passwords
```js

python main.py -l

```
## About
This is a simple & free password manager made using python that you can use to store your passwords securely. It uses fernet to encrypt the data entered.
This whole projet was created by Imira Randeniya. Development Process Is Currently Ongoing.
<br>
You can find the GUI Version Of ManageMyPasswords [here.](https://github.com/Imira-S-R/PasswordManager)

## License
Copyright (c) Imira Randeniya. All rights reserved.

Licensed under the [MIT License](./LICENSE).
