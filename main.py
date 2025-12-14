from log_hash import register_user, login_user

def menu():
    print('*'* 30)
    print('*** Welcome to my system ***')
    print('choose from the following options: ')
    print('1. Register')
    print('2. Login')
    print('3. Exit')
    print('*'* 30)

def main():
    while True:
        menu()
        choice = input("> ")
        if choice == '1':
            register_user()
            print("User registered successfully!")
        elif choice == '2':
            if login_user():
                print("Login successful!")
            else:
                print("Login failed! Invalid username or password.")
        elif choice == '3':
            print("Goodbye!")
            break

import sqlite3
import pandas as pd

sqlite3.connect


def create_user_table():
    curr = conn.cursor()

    sql = '''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL)'''


    curr.execute(sql)
    conn.commit()

def add_user(conn, name, hash_password):
    curr = conn.cursor()
    sql = '''INSERT INTO users (username, password_hash) VALUES (?, ?)'''
    parram = (name, hash_password)
    curr.execute(sql,parram)
    conn.commit()

def migrate_users():
    with open('DATA/user.txt', 'r') as f:
        users = f.readlines()

    for user in users:
        name, hash = user.strip().split(',')
        add_user(conn, name, hash) 
    conn



def get_all_users(conn):
    curr = conn.cursor()
    sql = "SELECT * from users"
    curr.execute(sql)
    users = curr.fetchall()
    conn.close()
    return(users)


def get_user(conn, name_):
    curr = conn.cursor()
    sql = "SELECT *  from users WHERE username = ?"
    param = (name_,)
    curr.execute(sql,param)
    user = curr.fetchall()
    conn.close()

    print(user)

def migrate_datasets_metadata(conn):
    data =  pd.read_csv('DATA/datasets_metadata.csv')
    data.to_sql('datasets_metadata', conn, if_exists='replace', index=False)
    conn.close()

def get_all_users_pandas(conn):
    sql = "SELECT * from datasets_metadata"
    data = pd.read_sql_query(sql, conn)
    return data

#INSERR, UPDATE, DELETE operations
conn = sqlite3.connect('DATA/intelligence_platform.db')
curr = conn.cursor()
sql = ""
parr = ""
curr.execute(sql,parr)
conn.commit()
conn.close()

#GET DATA from table
conn = sqlite3.connect('DATA/intelligence_platform.db')
curr = conn.cursor()
sql = ""
parr = ""
curr.execute(sql,parr)
conn.fetchall()
conn.fetchone()
conn.close()


with open('DATA/user.txt', 'r') as f:
    users = f.readlines()

for user in users:
    name, hash = user.strip().split(',')
    add_user(conn, name, hash)

conn.close()


conn = sqlite3.connect('DATA/intelligence_platform.db')