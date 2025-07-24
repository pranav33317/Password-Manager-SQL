import mysql.connector
import bcrypt
from cryptography.fernet import Fernet
from tabulate import tabulate
import random

# Generate and save this securely for production
fernet_key = Fernet.generate_key()
cipher = Fernet(fernet_key)

conn = mysql.connector.connect(host='localhost', user='root', passwd='123', charset="utf8")
cur = conn.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS project")
cur.execute("USE project")

cur.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        NO INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        Username VARCHAR(240) NOT NULL,
        Password TEXT,
        Email_linked VARCHAR(240),
        App_name VARCHAR(240)
    )
""")
cur.execute("ALTER TABLE passwords AUTO_INCREMENT=100")

cur.execute("""
    CREATE TABLE IF NOT EXISTS user (
        NO INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        Username VARCHAR(240) NOT NULL,
        Password VARBINARY(255)
    )
""")
cur.execute("ALTER TABLE user AUTO_INCREMENT=50")

# Insert master user if not already present
cur.execute("SELECT COUNT(*) FROM user")
if cur.fetchone()[0] == 0:
    hashed = bcrypt.hashpw("secret".encode(), bcrypt.gensalt())
    cur.execute("INSERT INTO user (Username, Password) VALUES (%s, %s)", ("jebin", hashed))
    conn.commit()


def adddata():
    while True:
        print("* Press enter to skip any field except Username *")
        username = input("Enter the username           : ")
        password = input("The password assigned         : ")
        email = input("The Email address linked      : ")
        app = input("The app name                  : ")

        if not username:
            print("Username is required.")
            continue

        enc_pass = cipher.encrypt(password.encode())

        try:
            conn.start_transaction()
            cur.execute(
                "INSERT INTO passwords (Username, Password, Email_linked, App_name) VALUES (%s, %s, %s, %s)",
                (username, enc_pass, email, app)
            )
            conn.commit()
            print("Data added successfully!")
        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")
        finally:
            op = input("👉 1 to add more | 2 to leave: ")
            if op == '2':
                break


def passwordgen():
    import random

    low = "abcdefghijklmnopqrstuvwxyz"
    upp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    num = "0123456789"
    sym = "!@#$%^&*"

    all_chars = low + upp + num + sym

    while True:
        try:
            length = int(input("Enter password length (min 4): "))
            if length < 4:
                print("Password length must be at least 4.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    # Ensure one of each category
    password = [
        random.choice(low),
        random.choice(upp),
        random.choice(num),
        random.choice(sym)
    ]

    # Fill the rest with random choices from all characters
    password += random.choices(all_chars, k=length - 4)

    # Shuffle to avoid predictable pattern
    random.shuffle(password)

    return ''.join(password)



def autogen():
    while True:
        username = input("Enter the username           : ")
        email = input("The Email address linked      : ")
        app = input("The app name                  : ")
        password = passwordgen()
        enc_pass = cipher.encrypt(password.encode())

        try:
            conn.start_transaction()
            cur.execute(
                "INSERT INTO passwords (Username, Password, Email_linked, App_name) VALUES (%s, %s, %s, %s)",
                (username, enc_pass, email, app)
            )
            conn.commit()
            print("Password generated =", password)
            print("Data added successfully!")
        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")
        finally:
            op = input("👉 1 to add more | 2 to leave: ")
            if op == '2':
                break


def display():
    try:
        cur.execute("SELECT * FROM passwords")
        data = cur.fetchall()
        decrypted_data = [
            (no, user, cipher.decrypt(password).decode(), email, app)
            for no, user, password, email, app in data
        ]
        print(tabulate(decrypted_data, headers=['NO', 'Username', 'Password', 'Email_linked', 'App_name'], tablefmt="grid"))
    except Exception as e:
        print(f"Error fetching data: {e}")


def search():
    app = input("Enter the app name to search: ")
    try:
        cur.execute("SELECT * FROM passwords WHERE App_name LIKE %s", (app,))
        data = cur.fetchall()
        decrypted_data = [
            (no, user, cipher.decrypt(password).decode(), email, app_name)
            for no, user, password, email, app_name in data
        ]
        print(tabulate(decrypted_data, headers=['NO', 'Username', 'Password', 'Email_linked', 'App_name'], tablefmt="grid"))
    except Exception as e:
        print(f"Error: {e}")


def removedetails():
    display()
    try:
        no = int(input("Enter the NO: "))
        app = input("Enter the app name: ")
        confirm = input("Are you sure? (y/n): ")
        if confirm.lower() == 'y':
            conn.start_transaction()
            cur.execute("DELETE FROM passwords WHERE NO = %s AND App_name = %s", (no, app))
            conn.commit()
            print("Data removed.")
        else:
            print("Operation cancelled.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")


def update_field(field):
    display()
    try:
        no = int(input("Enter the NO: "))
        app = input("Enter the App_name: ")
        new_val = input(f"Enter the new {field}: ")

        if field == "Password":
            new_val = cipher.encrypt(new_val.encode())

        conn.start_transaction()
        cur.execute(f"UPDATE passwords SET {field} = %s WHERE NO = %s AND App_name = %s", (new_val, no, app))
        conn.commit()
        print(f"{field} updated.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")


def changepass(): update_field("Password")
def changeuser(): update_field("Username")
def changeemail(): update_field("Email_linked")


def total():
    cur.execute("SELECT COUNT(*) FROM passwords")
    return cur.fetchone()[0]


def mainuser():
    new_user = input("Enter new master Username: ")
    try:
        cur.execute("UPDATE user SET Username = %s", (new_user,))
        conn.commit()
        print("Username updated.")
    except Exception as e:
        print(f"Error: {e}")


def mainpass():
    new_pass = input("Enter new master Password: ")
    hashed = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt())
    try:
        cur.execute("UPDATE user SET Password = %s", (hashed,))
        conn.commit()
        print("Password updated.")
    except Exception as e:
        print(f"Error: {e}")


def getuser():
    cur.execute("SELECT Username FROM user")
    return cur.fetchone()[0]


def getpass():
    cur.execute("SELECT Password FROM user")
    return cur.fetchone()[0]
