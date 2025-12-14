
import bcrypt

password = 'Magic123'

def hash_password(pasword):
    binary_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(binary_password, salt)
    return hash.decode('utf-8')

def validate_hash(password, hash):
    bin_pwd = password.encode('utf-8')
    bin_hash = hash.encode('utf-8')
    return bcrypt.checkpw(bin_pwd, bin_hash)

def register_user():
    user_name = input("Enter username: ")
    user_pwd = input("Enter password: ")
    hash = hash_password(user_pwd)
    with open("user.txt", "a") as f:
        f.write(f"{user_name},{hash}\n")

def login_user():
    user_name = input("Enter username: ")
    user_pwd = input("Enter password: ")
    with open("user.txt", "r") as f:
        users = f.readlines()

    for user in users:
        name, hash = user.strip().split(",")

        if user_name == name:
            return validate_hash(user_pwd, hash)
    return False