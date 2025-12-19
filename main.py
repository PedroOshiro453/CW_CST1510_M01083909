from log_hash import register_user, login_user


def menu():
    print("*" * 30)
    print("*** Welcome to my system ***")
    print("Choose from the following options: ")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    print("*" * 30)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "1":
            if register_user():
                print("User registered successfully!")
        elif choice == "2":
            if login_user():
                print("Login successful!")
            else:
                print("Login failed! Invalid username or password.")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()