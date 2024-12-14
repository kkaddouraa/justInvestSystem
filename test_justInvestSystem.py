# SYSC 4810 A Assignment
# Kareem Kaddoura
# 101140255

"""
Test cases for simulating the system's features, including the creation of a new user
(role-dependent), logging in a returning user, and overriding the system clock 
for Teller access.
"""

from role_operations import *
from security_methods import *

# Generate sample users provided in assignment doc
sample_users = [
    ["skim", "Skim000!", "Client"], # Sasha Kim
    ["eblake", "Ebla111@", "Client"], # Emery Blake
    ["nabbasi", "Nabb222#", "Premium Client"], # Noor Abblasim
    ["zadebayo", "Zade333$", "Premium Client"], # Zuri Adebayo
    ["mchen", "Mche444%", "Financial Advisor"], # Mikael Chen
    ["jriley", "Jril555*", "Financial Advisor"], # Jordan Riley
    ["enakamura", "Enak666&", "Financial Planner"], # Ellis Nakamura
    ["hdiaz", "Hdia777!", "Financial Planner"], # Harper Diaz
    ["ahayes", "Ahay888@", "Teller"], # Alex Hayes
    ["apatel", "Apat999#", "Teller"] # Adair Patel
]

for sample_user in sample_users:
    salt = generate_salt()
    hash_pw = hash_details(sample_user[1], salt)
    store_login_info(User(sample_user[0], salt, hash_pw, sample_user[2]))


"""
Test for creating a new user
"""
def test_create_user():
    salt = generate_salt()
    role = retrieve_role("1")
    hash_pw = hash_details("Password1!", salt)

    assert str(User("Test1", salt, hash_pw, role)) == f"Test1 | {salt} | {hash_pw} | {role}"

"""
Test for ensuring password upholds requirements
"""
def test_password_requirements():
    password1 = "John1!" # Less than 8 characters
    password2 = "John12345678!" # Exceeds 12 characters
    password3 = "john12345!" # Does not contain an uppercase character
    password4 = "JOHN12345!" # Does not contain a lowercase character
    password5 = "JohnJohn!" # Does not contain a digit
    password6 = "John123456" # Does not contain a special character
    password7 = "John123!" # Is found on the denylist
    password8 = "John1234$" # Meets all requirements
    
    assert check_password_requirements(password1) == False
    assert check_password_requirements(password2) == False
    assert check_password_requirements(password3) == False
    assert check_password_requirements(password4) == False
    assert check_password_requirements(password5) == False
    assert check_password_requirements(password6) == False
    assert check_password_requirements(password7) == False
    assert check_password_requirements(password8) == True

"""
Test for checking a role's permitted operations
"""
def test_role_operations():
    test1 = User("Test1", generate_salt(), hash_details("Password1!", generate_salt()), "Client")
    test2 = User("Test2", generate_salt(), hash_details("Password2!", generate_salt()), "Premium Client")
    test3 = User("Test3", generate_salt(), hash_details("Password3!", generate_salt()), "Financial Advisor")
    test4 = User("Test4", generate_salt(), hash_details("Password4!", generate_salt()), "Financial Planner")
    test5 = User("Test5", generate_salt(), hash_details("Password5!", generate_salt()), "Teller")

    # Client Tests
    assert test1.operations("1") == True
    assert test1.operations("5") != True
    # Premium Client Tests
    assert test2.operations("1") == True
    assert test2.operations("7") != True
    # Financial Advisor Tests
    assert test3.operations("1") == True
    assert test3.operations("6") != True
    # Financial Planner Tests
    assert test4.operations("1") == True
    assert test4.operations("7") != True
    # Teller Tests
    assert test5.operations("1") == True
    assert test5.operations("4") != True

"""
Test for verifying a returning user's login credentials
"""
def test_verify_login():
    # Using Sasha Kim as an example:
    assert verify_login("test_login", "Login123!") == False # Non-existent credentials
    assert verify_login("ski", "Skim000!") == False # Incorect Username
    assert verify_login("skim", "Skim00") == False # Incorect Password
    assert verify_login("skim", "Skim000!") == True # Correct Credentials

"""
Test for retrieving a user's details from passwd.txt, essentially confirming its existence
"""
def test_retrieve_account():
    # Using Harper Diaz as an example:
    assert retrieve_login_details("hdia", "Hdia777!") is None # Incorect Username
    assert retrieve_login_details("hdiaz", "Hdia7!") is None # Incorect Password
    assert retrieve_login_details("hdiaz", "Hdia777!") is not None # Correct Credentials

"""
Test for ensuring Teller access is only during business hours
"""
def test_business_hours():
    opening_time = dt.time(9,0,0) # 9:00 AM
    closing_time = dt.time(17,0,0) # 5:00 PM
    system_time = dt.datetime.now().time()
    if opening_time <= system_time <= closing_time:
        assert check_business_hours(system_time) == True
    else:
        assert check_business_hours(system_time) != True


if __name__ == '__main__':
    tests = [test_create_user, test_password_requirements, test_role_operations,
            test_verify_login, test_retrieve_account, test_business_hours]
    
    test_passed = 0

    for t in tests:
        try:
            t()
        except:
            print(t.__name__ + ": failed")
        else:
            print(t.__name__ + ": passed")
            test_passed += 1

    print(f"{test_passed} out of {len(tests)} tests have passed.")