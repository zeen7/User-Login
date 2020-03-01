import hashlib
import os.path
import sqlite3
from getpass import getpass

#database connection
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "account_database.db")
db_connection = sqlite3.connect(db_path)
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
    unverified_password=getpass("Enter a new password: ")
    new_password=getpass("Enter password again: ")

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

#Hash for passwords
def hash_target(new_password):
    new_password=hashlib.sha256(convert_to_bytes(new_password)).hexdigest()
    return new_password

#main method
def main(): 
    user_quit=False
    while(user_quit==False):
        choice=main_menu()
        #Login
        if choice==1:
            username_attempt=input("Enter your username: ")
            password_attempt=getpass("Enter your password: ")
            is_valid_credentials(username_attempt, password_attempt)
        #Create account
        elif choice==2:
            create_account()
        #Exit
        elif choice==3:
            print("Exited Account Login")
            user_quit=True
        else:
            print("Invalid Command")

if __name__ == '__main__':
    main()
