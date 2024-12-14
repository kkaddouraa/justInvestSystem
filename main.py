# SYSC 4810 A Assignment
# Kareem Kaddoura
# 101140255

"""
Main class to execute the system.
[Addresses Problem 3A]
"""

import datetime as dt
from security_methods import *

def print_intro():
    print()
    print("justInvest Portfolio Management")
    print("----------------------------------")
    print("Investing in your future securely.")
    print()

def main():
    system_time = dt.datetime.now().time()
    
    while True:
        print_intro()
        print("System Time: " + system_time.strftime("%H:%M\n"))
        print("Operations:\n1: New User\n2: Returning User\n3: Exit\n")
        action = input("> ")
        print()

        # New User, [Addresses Problem 3A]
        if action == "1":
            print("Which role would you like to register for?")
            print("1: Client\n2: Premium Client\n3: Financial Adivsor\n4: Financial Planner\n5: Teller\n")
            role = input("> ")
            print()
            if role not in ["1", "2", "3", "4", "5"]:
                print("Invalid operation, please try again.\n")
            else:
                new_user = create_new_user(role)
                store_login_info(new_user)
                
        # Returning User, [Addresses Problem 4A]
        elif action == "2":
            returning_user = login_user()
            if returning_user is None:
                print("\nYou have reached the maximum number of tries. Try again later.\n")
            else:
                if returning_user.role == "Teller":
                    if check_business_hours(system_time) is not True:
                        print("Override System Clock? (yes/no)\n")
                        clock_override = input("> ").casefold()
                        if clock_override == "yes":
                            system_time = modify_business_hours()
                        elif clock_override == "no":
                            pass
                            print()
                        else:
                            print("Invalid operation, please try again.\n")
                    else:
                        login_user_session(returning_user)
                else:
                    login_user_session(returning_user)
            
        # Exit
        elif action == "3":
            print("Thank you for your loyalty, have a pleasant day.\n")
            break
        else:
            print("Invalid operation, please try again.\n")

main()