import passs
import os
import time
import bcrypt

# Fetch username and hashed password from DB
username = passs.getuser()
password_hash = passs.getpass()  # hashed (binary)

print("--PASSWORD MANAGER--".center(71, "🔑"))
print("^^^^^^^^^^^^^^^^^")

# First login attempt
user = input("Enter your username     :: ")
pas = input("Enter your password     :: ")
print("^^^^^^^^^^^^^^^^^")

# Validate credentials
if user != username or not bcrypt.checkpw(pas.encode(), password_hash):
    print("\nIncorrect username or password.")
    print("Retry in 5 seconds...*WARNING!!! ONLY ONE MORE CHANCE!!!!*")
    for i in range(1, 6):
        print(i, " >> ", end="")
        time.sleep(1)

    print("\n\n^^^^^^^^^^^^^^^^^")
    user = input("Enter your username     :: ")
    pas = input("Enter your password     :: ")
    print("^^^^^^^^^^^^^^^^^")

    if user != username or not bcrypt.checkpw(pas.encode(), password_hash):
        print("\n⚠⚠⚠ Incorrect username or password ⚠⚠⚠")
        print("No more chances. Exiting in:")
        for i in range(1, 3):
            print(i, " >> ", end="")
            time.sleep(1)
        exit()

# Main menu loop
while True:
    print("\n🎇__________________________ MAIN MENU __________________________🎇")
    print("🔐" + "*" * 65 + "🔐")
    print("👉 1. ADD DETAILS")
    print("👉 2. EDIT DETAILS")
    print("👉 3. REMOVE DETAILS")
    print("👉 4. VIEW ALL")
    print("👉 5. AUTO GENERATE PASSWORD")
    print("👉 6. SEARCH")
    print("👉 7. APP SETTINGS")
    print("👉 8. EXIT")
    print("🔐" + "*" * 65 + "🔐\n")

    try:
        option = int(input("Enter your option:: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    if option == 1:
        print("\n" + "⚙" * 20)
        print("a. ADD MANUAL ENTRY")
        print("b. ADD WITH AUTO PASSWORD")
        print("c. RETURN TO MAIN MENU")
        print("⚙" * 20 + "\n")

        optionevent = input("Enter your option:: ").lower()

        if optionevent == "a":
            passs.adddata()
        elif optionevent == "b":
            passs.autogen()
        elif optionevent == "c":
            print("<< Returning to main menu >>")
        else:
            print("Invalid option!")

    elif option == 2:
        if passs.total() == 0:
            print("\nNo details added yet!\n")
        else:
            print("\n" + "🛠" * 20)
            print("a. CHANGE PASSWORD")
            print("b. CHANGE USERNAME")
            print("c. CHANGE EMAIL")
            print("d. RETURN TO MAIN MENU")
            print("🛠" * 20 + "\n")

            optioncar = input("Enter your option:: ").lower()

            if optioncar == "a":
                passs.changepass()
            elif optioncar == "b":
                passs.changeuser()
            elif optioncar == "c":
                passs.changeemail()
            elif optioncar == "d":
                print("<< Returning to main menu >>")
            else:
                print("Invalid option!")

    elif option == 3:
        if passs.total() == 0:
            print("\nNo details added yet!\n")
        else:
            passs.removedetails()

    elif option == 4:
        if passs.total() == 0:
            print("\nNo details added yet!\n")
        else:
            passs.display()

    elif option == 5:
        print("\n⚠ Your generated password is:", passs.passwordgen(), "\n")

    elif option == 6:
        if passs.total() == 0:
            print("\nNo details added yet!\n")
        else:
            passs.search()

    elif option == 7:
        while True:
            print("1. CHANGE MASTER PASSWORD")
            print("2. CHANGE MASTER USERNAME")
            print("3. RETURN TO MAIN MENU\n")

            try:
                us = int(input("Your option is :: "))
            except ValueError:
                print("Invalid input. Enter a number.")
                continue

            if us == 1:
                oldp = input("Enter your existing password: ")
                if bcrypt.checkpw(oldp.encode(), password_hash):
                    passs.mainpass()
                    print("\n<< Password updated successfully >>\n")
                    password_hash = passs.getpass()  # refresh hash
                else:
                    print("\n⚠ Old password does not match ⚠\n")

            elif us == 2:
                old_user = input("Enter your existing username: ")
                old_pass = input("Enter your existing password: ")
                if old_user == username and bcrypt.checkpw(old_pass.encode(), password_hash):
                    passs.mainuser()
                    print("\n<< Username updated successfully >>\n")
                    username = passs.getuser()  # refresh username
                else:
                    print("\n⚠ Incorrect current credentials ⚠\n")

            elif us == 3:
                print("<< Returning to main menu >>\n")
                break
            else:
                print("Invalid option!")

    elif option == 8:
        print("\nWe keep all your details safe. Thank you!")
        print("Exiting in:")
        for i in range(1, 6):
            print(i, " >> ", end="")
            time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        break

    else:
        print("Please enter a valid menu option (1-8)!")
