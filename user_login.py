import hashlib
import json
import sqlite3

#database connection
db_connection = sqlite3.connect('C:\\Users\\zeen-\\OneDrive\\桌面\\User Login\\database.db')
c = db_connection.cursor()

#SHA256 hashing
hash1=hashlib.sha256()

#Checks if username and password is valid
def is_valid_credentials(username_try, password_try):
    c.execute('SELECT * FROM users;')
    for x in range (len(c.fetchall())):
        c.execute("SELECT password_hash FROM users WHERE username='"+username_try+"';")
        pw_db = c.fetchall()
        pw_db=[i[0] for i in pw_db]

        if len(pw_db)>0:
            if pw_db[0]==hash_target(password_try):
                print("Correct credentials")
                return True
            else:
                print("Invalid username or password")
                return False
        else:
            print("Invalid username or password")
            return False

#initial menu
def main_menu():
    while True:
        try:
            login_choice=int(input("Enter 1 if you have an account. Enter 2 if you want to create an account. Enter 3 to quit.\n"))
            if (login_choice!=1 and login_choice!=2 and login_choice!=3):
                raise ValueError
            break

        except ValueError:
            print(type(login_choice))
            print("Input Error")

    return login_choice

#Creates a new account
def create_account():
    new_username=input("Enter a new username: ")
    unverified_password=input("Enter a new password: ")
    new_password=input("Enter password again: ")

    if (unverified_password==new_password):
        #check if username is taken
        c.execute('SELECT * FROM users;')
        for x in range (len(c.fetchall())):
            c.execute('SELECT username FROM users;')
            username_db = c.fetchall()
            username_db = [i[0] for i in username_db]
            c.execute('SELECT password_hash FROM users;')
            password_db = c.fetchall()
            password_db = [j[0] for j in password_db]

            #convert new password to hash
            new_password_hash=hash_target(new_password)
                    
            if new_username==username_db[x] or new_password_hash==password_db[x]:
                print("Username or password already taken")

            #add new username and password to database
            else:
                c.execute("INSERT INTO users (username, password_hash) "+ "VALUES ('"+new_username+"', '"+ new_password_hash+"');")
                # Save (commit) the changes
                db_connection.commit()
                print("Account successfully created")
                break

    #if password verify does not match password initally entered
    else:
        print("Password does not match")
        

#Converts string to bytes for hashing
def convert_to_bytes(pw):
    result=str.encode(pw)
    return result

def hash_target(new_password):
    hash1.update(convert_to_bytes(new_password))
    return hash1.hexdigest()

#main method
def main():
    choice=main_menu()
    if choice==1:
        #Prompts user to enter username and password
        username_attempt=input("Enter your username: ")
        password_attempt=input("Enter your password: ")
        is_valid_credentials(username_attempt, password_attempt)
    elif choice==2:
        create_account()
        print("\n")
        #Prompts user to enter username and password
        username_attempt=input("Enter your username: ")
        password_attempt=input("Enter your password: ")
        is_valid_credentials(username_attempt, password_attempt)
    elif choice==3:
        print("Exited Account Login")

main()
