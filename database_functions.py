#!/usr/bin/python

import psycopg2
from config import config
from connect import connect
from termcolor import cprint, colored
import colorama
import subprocess

from encryption import decryptString, encryptString

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE passwords_information_table (
        password_id serial PRIMARY KEY,
        website_name TEXT UNIQUE NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE user_information (
        id serial PRIMARY KEY,
        master_pswd TEXT UNIQUE NOT NULL
        );
        """
        )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_password(website_name, username, password):
    """ insert a new vendor into the vendors table """
    sql = """
    INSERT INTO 
    passwords_information_table (website_name, username, password)
    VALUES(%s, %s, %s) RETURNING password_id;
    """
    conn = None
    password_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (website_name, username, password,))
        # get the generated id back
        password_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return password_id


def insert_master_password(password):
    """ insert a new vendor into the vendors table """
    sql = """
    INSERT INTO 
    user_information (master_pswd)
    VALUES(%s) RETURNING id;
    """
    conn = None
    password_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (password,))
        # get the generated id back
        password_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def delete_password (password_id) :
    sql = f"""
    DELETE FROM passwords_information_table WHERE "password_id" = {password_id};
    """
    conn = None
    password_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        cur.execute(sql, (password_id))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return password_id

def get_records():
    # SQL to get records from Postgres
    s = "SELECT * FROM passwords_information_table"
    # Error trapping
    conn = None
    list_users = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # Execute the SQL
        cur.execute(s)
        # Retrieve records from Postgres into a Python List
        list_users = cur.fetchall()
    except psycopg2.Error as e:
        t_message = "Database error: "
        print(t_message)
    
    # Close the database cursor and connection
    cur.close()
    conn.close()

    return list_users

def get_master_pswd():
    # SQL to get records from Postgres
    s = "SELECT * FROM user_information"
    # Error trapping
    conn = None
    list_users = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # Execute the SQL
        cur.execute(s)
        # Retrieve records from Postgres into a Python List
        list_users = cur.fetchall()
    except psycopg2.Error as e:
        t_message = "Database error: "
        print(t_message)
    
    # Close the database cursor and connection
    cur.close()
    conn.close()

    return list_users


def get_specific_records(key, website_name):
    # SQL to get records from Postgres
    s = f"""SELECT * FROM passwords_information_table;"""
    # Error trapping
    conn = None
    list_passwords = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # Execute the SQL
        cur.execute(s)
        # Retrieve records from Postgres into a Python List
        list_passwords = cur.fetchall()

        for password in list_passwords:
            if decryptString(key, password[1]) == website_name:
                print('')
                cprint(f'{decryptString(key, password[3])}', "green")
                print('')
                copy2clip(decryptString(key, password[3]))
                cprint('(The Password Has Been Copied To Your Clipboard)', "white")
            else:
                cprint(f'No Password Found For {website_name}')
    except psycopg2.Error as e:
        t_message = "Database error: "
        print(t_message)
    
    # Close the database cursor and connection
    cur.close()
    conn.close()

def get_specific_info (id) :
    # SQL to get records from Postgres
    s = f"""SELECT * FROM passwords_information_table WHERE password_id='{id}';"""
    # Error trapping
    conn = None
    list_passwords = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # Execute the SQL
        cur.execute(s)
        # Retrieve records from Postgres into a Python List
        list_passwords = cur.fetchall()
        return list_passwords
    except psycopg2.Error as e:
        t_message = "Database error: "
        print(t_message)
    
    # Close the database cursor and connection
    cur.close()
    conn.close()




def update_passwords(password_id, website_name, username, password):
    """ update vendor name based on the vendor id """
    sql = """UPDATE passwords_information_table
              SET website_name = %s, 
              username = %s, 
              password = %s
              WHERE password_id = %s;
              """
    conn = None
    updated_rows = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (website_name, username, password, password_id))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


if __name__ == '__main__':
    #   create_tables()
#     # insert_password('google.com', 'imira', 'hello')
#     # update_passwords(1, 'facebook.com', 'imira@imira.com', '12345')
#     # delete_password(1)
      print()