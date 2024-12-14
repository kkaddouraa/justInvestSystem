# SYSC 4810 A Assignment
# Kareem Kaddoura
# 101140255

"""
Responsible for all operations that can be executed by each role. Uses a RBAC system to
ensure permission seperation. Used only for visual and testing purposes, the actual
operations themselves print random values to simulate their actual functionality.


Glossary
- ab = Account Balance
- ip = Investment Portfolio
- fa = Financial Advisor
- fp = Financial Planner
- pci = Private Consumer Instruments
- mmi = Money Market Instruments
"""

import random

num_to_role_dict = {
    "1": "Client",
    "2": "Premium Client",
    "3": "Financial Advisor",
    "4": "Financial Planner",
    "5": "Teller"
}

def retrieve_role(role_num):
    return num_to_role_dict.get(role_num)

class User:
    def __init__(self, username, salt, hash, role):
        self.username = username
        self.salt = salt
        self.hash = hash
        self.role = role
        self.active = True # Activate Login Session
        
        # Sample data for user operations
        if role == "Client" or role == "Premium Client": 
            self.random_balance = random.randint(5000, 70000)
            self.random_initial_investment = random.randint(1000, 5000)
            self.random_current_investment = random.randint(7000, 15000)
            self.random_fa = random.choice(["Mikael Chen", "Jordan Riley"])
        if role == "Premium Client":
            self.random_fp = random.choice(["Ellis Nakamura", "Harper Diaz"])
        if role == "Financial Advisor" or role == "Financial Planner" or role == "Teller":
            self.random_client = random.choice(["Sasha Kim", "Emery Blake", "Noor Abblasim", "Zuri Adebayo"])
        if role == "Financial Advisor" or role == "Financial Planner":
            self.pci = "- Bonds\n- Investments\n- Payable Loans"
        if role == "Financial Planner":
            self.mmi = "- Loans\n- Mutual Funds\n- Treasury Bills"

    """
    String format of User that is stored in passwd.txt
    [Addresses Problem 2B]
    """
    def __str__(self):
        return f"{self.username} | {self.salt} | {self.hash} | {self.role}" # Format for passwd.txt placement
    
    def print_user_info(self):
        print(self.username + " | " + self.role + "\n")

    """
    Available operations to the user depending on their role
    [Addresses Problem 4B]
    """
    def print_available_operations(self):
        permitted_operations = {
            "Client": {
                "1": "View Account Balance",
                "2": "View Investment Portfolio",
                "3": "View Financial Advisor Contact Details",
                "4": "Logout"
            },
            "Premium Client": {
                "1": "View Account Balance",
                "2": "View Investment Portfolio",
                "3": "Modify Investment Portfolio",
                "4": "View Financial Advisor Contact Details",
                "5": "View Financial Planner Contact Details",
                "6": "Logout"
            },
            "Financial Advisor": {
                "1": "View Client Account Balance",
                "2": "View Client Investment Portfolio",
                "3": "Modify Client Investment Portfolio",
                "4": "View Private Consumer Instruments",
                "5": "Logout"
            },
            "Financial Planner": {
                "1": "View Client Account Balance",
                "2": "View Client Investment Portfolio",
                "3": "Modify Client Investment Portfolio",
                "4": "View Private Consumer Instruments",
                "5": "View Money Market Instruments",
                "6": "Logout"
            },
            "Teller": {
                "1": "View Client Account Balance",
                "2": "View Client Investment Portfolio",
                "3": "Logout"
            }
        }
        operation = permitted_operations.get(self.role)
        print("Operations:")
        for op_num, op in operation.items():
            print(f"{op_num}: {op}")
        print()

    """
    View Account Balance
    Permitted users: Client, Premium Client
    [Sample Purposes]
    """
    def view_ab(self):
        if self.role == "Client" or self.role == "Premium Client":
            print("\nBalance: $" + str(self.random_balance) + "\n")

    """
    View Investment Portfolio
    Permitted users: Client, Premium Client
    [Sample Purposes]
    """
    def view_ip(self):
        if self.role == "Client" or self.role == "Premium Client":
            print("\nInvestment: $" + str(self.random_initial_investment))
            print("Value: $" + str(self.random_current_investment) + "\n")

    """
    View Financial Advisor Contact Info
    Permitted users: Client, Premium Client
    [Sample Purposes]
    """
    def view_fa_info(self):
        if self.role == "Client" or self.role == "Premium Client":
            print("\nDesignated Financial Adivsor: " + str(self.random_fa) + "\n")

    """
    View Financial Planner Contact Info
    Permitted users: Premium Client
    [Sample Purposes]
    """
    def view_fp_info(self):
        if self.role == "Premium Client":
            print("\nDesignated Financial Planner: " + str(self.random_fp) + "\n")

    """
    Modify Investment Porfolio
    Permitted users: Premium Client
    [Sample Purposes]
    """
    def modify_ip(self):
        if self.role == "Premium Client":
            self.random_initial_investment = input("\nNew investment: $")
            self.view_ip()

    """
    View Client Account Balance
    Permitted users: Financial Advisor, Financial Planner, Teller
    [Sample Purposes]
    """
    def view_client_ab(self):
        if self.role == "Financial Advisor" or self.role == "Financial Planner" or self.role == "Teller":
            print("\nClient: " + str(self.random_client))
            print("Balance: $" + str(random.randint(5000, 70000)) + "\n")

    """
    View Client Investment Portfolio
    Permitted users: Financial Advisor, Financial Planner, Teller
    [Sample Purposes]
    """
    def view_client_ip(self):
        if self.role == "Financial Advisor" or self.role == "Financial Planner" or self.role == "Teller":
            print("\nClient: " + str(self.random_client))
            print("Investment: $" + str(random.randint(1000, 5000)))
            print("Value: $" + str(random.randint(7000, 15000)) + "\n")

    """
    Modify Client Investment Portfolio
    Permitted users: Financial Advisor, Financial Planner
    [Sample Purposes]
    """
    def modify_client_ip(self):
        if self.role == "Financial Advisor" or self.role == "Financial Planner":
            print("\nClient: " + str(self.random_client))
            input("New investment: $")
            print("Value: $" + str(random.randint(7000, 15000)) + "\n")

    """
    View Private Consumer Instruments
    Permitted users: Financial Advisor, Financial Planner
    [Sample Purposes]
    """
    def view_pci(self):
        if self.role == "Financial Advisor" or self.role == "Financial Planner":
            print("\nAvailable Private Consumer Instruments:")
            print(str(self.pci) + "\n")

    """
    View Money Market Instruments
    Permitted users: Financial Planner
    [Sample Purposes]
    """
    def view_mmi(self):
        if self.role == "Financial Planner":
            print("\nAvailable Money Market Instruments:")
            print(str(self.mmi) + "\n")
    
    """
    End user live session
    """
    def logout(self):
        self.active = False
        print("\nGoodbye, " + self.username + ".\n")

    def get_session_status(self):
        return self.active

    """
    Role-Based Access Control System (RBAC)
    A dictionary containing available roles in the system, where each role
    has certain operations that are only available to their role.
    By cross-referencing role operation priveleges and the user's account,
    the method needed is returned and executed. 
    [Addresses Problem 1C]
    """
    def operations(self, op_num):
        available_operations = {
            "Client": {
                "1": self.view_ab,
                "2": self.view_ip,
                "3": self.view_fa_info,
                "4": self.logout
            },
            "Premium Client": {
                "1": self.view_ab,
                "2": self.view_ip,
                "3": self.modify_ip,
                "4": self.view_fa_info,
                "5": self.view_fp_info,
                "6": self.logout
            },
            "Financial Advisor": {
                "1": self.view_client_ab,
                "2": self.view_client_ip,
                "3": self.modify_client_ip,
                "4": self.view_pci,
                "5": self.logout
            },
            "Financial Planner": {
                "1": self.view_client_ab,
                "2": self.view_client_ip,
                "3": self.modify_client_ip,
                "4": self.view_pci,
                "5": self.view_mmi,
                "6": self.logout
            },
            "Teller": {
                "1": self.view_client_ab,
                "2": self.view_client_ip,
                "3": self.logout
            }
        }

        role_ops = available_operations.get(self.role)
        if op_num in role_ops:
            role_ops[op_num]()
            return True
        else:
            print("Invalid operation, please try again.\n")

