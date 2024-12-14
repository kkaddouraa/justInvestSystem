# SYSC 4810 A Assignment
# Kareem Kaddoura
# 101140255

"""
Contains all security features available in the system. Ensures password requirements are
met, business hours are implemented (for Teller users), and proper user credentials are
stored efficiently and retrieved when neccesary. 

For hashing, hashlib.pbkdf2_hmac() is
used in combination with a SHA-256 algorithm.
"""

import os
import datetime as dt
import hashlib as hl

from role_operations import *

# Ensuring that passwd.txt and denylist.txt are used within the same directory as other files
current_directory = os.path.dirname(os.path.realpath(__file__))
passwd_file = os.path.join(current_directory, "passwd.txt")
denylist_file = os.path.join(current_directory, "denylist.txt")

def print_title():
    print()
    print("justInvest Portfolio Management")
    print("----------------------------------")
    print()

"""
Check business hours, used to ensure Teller access
"""
def check_business_hours(time):
    opening_time = dt.time(9,0,0) # 9:00 AM
    closing_time = dt.time(17,0,0) # 5:00 PM
    if opening_time <= time <= closing_time:
         return True
    else:
        print("\nLogin only permitted between 9:00 - 17:00")
        print("The current time is: " + time.strftime("%H:%M\n"))

"""
Ability to override system clock, used to ensure Teller access
"""
def modify_business_hours():
    new_time = input("\nNew System Time (HH:MM) [24H format]: ")
    print()
    return dt.datetime.strptime(new_time, "%H:%M").time()

"""
Create a new user for the system.
Takes care of systematic checks to ensure requirements are met.
"""
def create_new_user(role):
    while True:
        user = input("Username: ")
        if _check_username_is_unique(user):
            break
        else:
            print("\nUsername " + user + " is already taken!\n")
    while True:
        print_password_requirements()
        pw = input("Password: ")
        print()
        if check_password_requirements(pw) and pw != user:
            break
        else:
            print("\nPassword does not follow requirements!\n")
    salt = generate_salt()
    hash_pw = hash_details(pw, salt)
    return User(user, salt, hash_pw, retrieve_role(role))

"""
Ensure username is unique, checks passwd.txt for stored usernames
"""
def _check_username_is_unique(username):
    try:
        with open(passwd_file, "r") as file:
            for account in file:
                if account.split(" | ")[0] == username:
                    return False
        return True
    except Exception as e:
        print(e)
    finally:
        file.close()

def print_password_requirements():
    print()
    print("Passwords must:")
    print("- Be between 8 and 12 characters")
    print("- Contain at least 1 upper-case letter")
    print("- Contain at least 1 lower-case letter")
    print("- Contain at least 1 digit (0-9)")
    print("- Contain at least 1 special character (!,@,#,$,%,*,&)")
    print("- Not be commonly guessed or weak")
    print("- Not match the username")
    print()

"""
Ensure password meets requirements as outlined in assignment doc
"""
def check_password_requirements(password):
    special_chars = "!@#$%*&"
    condition1 = 8 <= len(password) <= 12
    condition2 = any(letter.isupper() for letter in password)
    condition3 = any(letter.islower() for letter in password)
    condition4 = any(letter.isdigit() for letter in password)
    condition5 = any(letter in special_chars for letter in password)
    condition6 = _check_password_denylist(password)
    if condition1 and condition2 and condition3 and condition4 and condition5 and condition6:
        return True
    else:
        return False

"""
Ensures proactive password checking, cross references password with denylist passwords
[Addresses Problem 3B]
"""
def _check_password_denylist(password):
    try:
        with open(denylist_file, "r") as file:
            for weak_password in file:
                if weak_password.strip() == password:
                    return False
        return True
    except Exception as e:
        print(e)
    finally:
        file.close()

"""
Generates random 32-byte salt
"""
def generate_salt():
    return os.urandom(32)

"""
Creates and returns Hash(password, salt)
[Addresses Problem 2A]
"""
def hash_details(pw, salt):
    hash_pw = hl.pbkdf2_hmac('sha256', pw.encode(), salt, 200000)
    return hash_pw

"""
Stores user details (u, s, H(p, s)) in passwd.txt
"""
def store_login_info(user):
    try:
        with open(passwd_file, "a") as file:
            if _check_username_is_unique(user.username):
                file.write(str(user) + "\n")
    except Exception as e:
        print(e)
    finally:
        file.close()

"""
Verifies and returns user login information
Implements basic form of throttling, limits users to 5 login attempts
"""
def login_user():
    max_tries = 5
    while True:
        if max_tries == 0:
            break

        user = input("Username: ")
        pw = input("Password: ")
        if verify_login(user, pw):
            return retrieve_login_details(user, pw)
        else:
            max_tries -= 1
            print("\nIncorrect credentials / Credentials not found, try again.")
            print("Remaining tries: " + str(max_tries) + "\n")

"""
Verifies user login information against passwd.txt; ensuring user exists and credentials are correct
"""
def verify_login(username, password):
    try:
        with open(passwd_file, "r") as file:
            for account in file:
                account_details = account.split(" | ")

                if account_details[0] == username:
                    salt = eval(account_details[1])
                    hash_pw = hash_details(password, salt)
                    if str(hash_pw) == account_details[2]:
                        return True
        return False
    except Exception as e:
        print(e)
    finally:
        file.close()

"""
Retrieve user details from passwd.txt
"""
def retrieve_login_details(username, password):
    try:
        with open(passwd_file, "r") as file:
            for account in file:
                account_details = account.split(" | ")

                if account_details[0] == username:
                    salt = eval(account_details[1])
                    hash_pw = hash_details(password, salt)
                    if str(hash_pw) == account_details[2]:
                        role = account_details[3].strip()
                        returning_user = User(username, salt, hash_pw, role)
                        return returning_user

    except Exception as e:
        print(e)
    finally:
        file.close()

"""
Establish live session for user to conduct their business
"""
def login_user_session(user):
    while user.get_session_status():
        print_title()
        user.print_user_info()
        user.print_available_operations()
        user.operations(input("> "))

