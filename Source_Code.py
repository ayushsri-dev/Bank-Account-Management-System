import random
import mysql.connector

# Database connection — adjust credentials as needed.

def db_connection():
    global con, cursor
    try:
        con = mysql.connector.connect(host='localhost', user='root', passwd='tiger')
        cursor = con.cursor()

    except mysql.connector.Error as err:    
        print("Error: Could not connect to database. Ensure MySQL server is running and credentials are correct.")
        exit()


# Create database and required tables if they do not exist.
# Profile stores user personal data; Account stores account metadata (PIN stored in plaintext here — not secure).

def create_database_table():
    try:
        cursor.execute("CREATE DATABASE Bank_Account_Management")
        cursor.execute("USE Bank_Account_Management")
        table1 = "CREATE TABLE Profile(Name varchar(50), Age integer, Phone BIGINT, Email varchar(100), Adhaar BIGINT)"
        cursor.execute(table1)
        table2 = "CREATE TABLE Account(Account_No integer, PIN integer, Account_Type varchar(50), Status varchar(50))"
        cursor.execute(table2)
    
    except Exception as e:
        print("Database and tables already exist. Proceeding...")
        
# Registration flow: collect user info, insert into Profile and Account tables, display generated account details.

def registration():
    print()
    print("=========== REGISTRATION ===========")
    name = input("Enter User Name : ")
    age = int(input("Enter Age :" ))
    phone = int(input("Enter phone : "))
    eid = input("Enter email id : ")
    reg = "INSERT INTO Profile(Name,Age,Phone,Email) VALUES('{}',{},{},'{}')".format(name, age, phone, eid)
    cursor.execute(reg)
    con.commit()
    print()
    print("User registration for a bank account has been successful. Kindly enter the requisite details.")
    print()
    accno = random.randint(10000000, 99999999)
    print("YOUR ACCOUNT NUMBER HAS BEEN GENERATED :", accno)
    pin = int(input("Create a 6 digit PIN : "))
    print("Kindly select your bank account type : ")
    print("1. Savings account")
    print("2. Current account")
    print("3. Fixed Deposit Account")
    print("4. Recurring Deposit Account")
    print("5. Demat Account")
    acc= {1:"Savings",2:"Current",3:"Fixed Deposit",4:"Recurring Deposit",5:"Demat"}
    cho = int(input("Enter your account type : "))
    print()
    print("Dear", name, ", you have successfully registered for a", acc[cho], "account.")
    stat = "ACTIVE"
    reg2 = "INSERT INTO Account(Account_No,PIN,Account_Type,Status) VALUES({},{},'{}','{}')".format(accno, pin,acc[cho] , stat)
    cursor.execute(reg2)
    con.commit()

    # Fetch and display the saved profile and account info.

    print()
    print("*********** ACCOUNT DETAILS ************")
    cursor.execute("SELECT Name,Age,Phone,Email from Profile WHERE Name='{}'".format(name))
    data = cursor.fetchall()
    print("User Name :", data[0][0])
    print("Age :", data[0][1])
    print("Phone :", data[0][2])
    print("Email :", data[0][3])
    cursor.execute("SELECT Account_No,PIN,Account_Type,Status from Account WHERE Account_No={}".format(accno))
    data = cursor.fetchall()
    print("Account Number :", data[0][0])
    print("PIN : XXX", (data[0][1]) % 1000)           # Only partially display PIN for privacy.
    print("Account Type :", data[0][2], "Account")
    print("Status :", data[0][3])
    print("*" * 39)
    menu()

# Sign-in: verify user exists and account exists, present post-login options.

def signin():
    print()
    print("=========== SIGN IN ===========")
    nm = input("Enter User Name : ")
    cursor.execute("SELECT* FROM Profile WHERE Name='{}'".format(nm))
    data = cursor.fetchall()
    count = cursor.rowcount
    acc = int(input("Enter Account Number : "))
    cursor.execute("SELECT* FROM Account WHERE Account_No={}".format(acc))
    data2 = cursor.fetchall()
    count2 = cursor.rowcount
    if count == 0 or count2 == 0:
        print()
        print("USER NOT FOUND. Exiting the system....")
        menu()
    else:
        print("Signed in Successfully!")
        print()
        print("1. Change PIN")
        print("2. KYC Update")
        print("3. Link with Adhaar")
        print("4. Transfer Account")
        print("5. Return to Homepage")
        print("6. Sign Out")
        chc = int(input("Enter your choice : "))
        print()

        # Change PIN: update Account table after OTP confirmation.
        if chc == 1:
            print("-" * 11, "CHANGE PIN", "-" * 11)
            print()
            newpin = int(input("Enter new PIN : "))
            cmd = "UPDATE Account SET PIN={} WHERE Account_No= {}".format(newpin, acc)
            otp = random.randint(1000, 9999)
            print("OTP :", otp)
            check = int(input("Enter OTP : "))
            if check == otp:
                cursor.execute(cmd)
                con.commit()
                print("PIN updated Successfully!")
                print("*" * 39)
                menu()
            else:
                print("Invalid OTP!")
                menu()
            
        # KYC update: update profile fields.
        elif chc == 2:
            print("-" * 11, "KYC UPDATE", "-" * 11)
            print()
            newname = input("Enter new username : ")
            newage = int(input("Enter new age : "))
            newph = int(input("Enter new phone : "))
            neid = input("Enter new email : ")
            cmd = "UPDATE Profile SET Name='{}', Age={}, Phone={}, Email='{}' WHERE Name= '{}'".format(newname, newage, newph, neid, nm)
            cursor.execute(cmd)
            con.commit()
            print()
            print("Your Details have been Updated Successfully!")
            menu()

        # Link Aadhaar with OTP confirmation.
        elif chc == 3:
            print("-" * 11, "LINK WITH ADHAAR", "-" * 11)
            print()
            adhpan = int(input("Enter ADHAAR : "))
            cmd = "UPDATE Profile SET Adhaar={} WHERE Name='{}'".format(adhpan, nm)
            otp = random.randint(1000, 9999)
            print("OTP:", otp)
            check = int(input("Enter OTP : "))
            if check == otp:
                cursor.execute(cmd)
                con.commit()
                print("ADHAAR details have been updated successfully!")
                menu()

        # Transfer account: overwrite profile with new user info after OTP confirmation.
        elif chc == 4:
            print("-" * 11, "TRANSFER ACCOUNT", "-" * 11)
            print("Register for new user : ")
            newuser = input("Name : ")
            nage = int(input("Age : "))
            nphone = int(input("Phone : "))
            nadh = int(input("ADHAAR : "))
            neweid = input("Email : ")
            cmd = "UPDATE Profile SET Name='{}',Age={},Phone={},Adhaar={},Email='{}' WHERE Name='{}'".format(newuser, nage, nphone, nadh, neweid, nm)
            otp = random.randint(1000, 9999)
            print("OTP :", otp)
            check = int(input("Enter OTP : "))
            if check == otp:
                cursor.execute(cmd)
                con.commit()
                print("Dear,", nm, ", your account has been transferred to", newuser)
                print("*" * 39)
                menu()

        # Return to main menu without changes.
        elif chc == 5:
            menu()

        # Sign out message.
        elif chc == 6:
            print("You have been successfully signed out.")
            menu()

        else:
            print("INVALID COMMAND.Exiting the system....")
            menu()

# Delete account: remove user from Profile and Account tables after OTP confirmation.

def delacc():
    print()
    print("-" * 11, "DELETE ACCOUNT", "-" * 11)
    nm = input("Enter user name : ")
    acno = int(input("Enter account number :"))
    ans = input("Are you sure want to delete account? (Yes/NO) : ")
    if ans == "Yes":
        otp = random.randint(1000, 9999)
        print("OTP :", otp)
        check = int(input("Enter otp : "))
        if check == otp:
            cursor.execute("DELETE FROM Profile WHERE Name='{}'".format(nm))
            con.commit()
            cursor.execute("DELETE FROM Account WHERE Account_No={}".format(acno))
            con.commit()
            cursor.execute("UPDATE Account SET Status='{}' WHERE Account_No={}".format('Deactive', acno))
            con.commit()
            print("Your Account has been deleted!")
            print("*" * 40)
            menu()
    else:
        print("*" * 40)
        menu()

# Exit: close DB connection and exit program.

def exit_program():
    print()
    print("-" * 11, "EXIT", "-" * 11)
    print("Thank you for using our system.Goodbye!")
    cursor.close()
    con.close()

# Main menu: present options to user.

def menu():
    print()
    print("─" * 10, "🗂️  MAIN MENU  🗂️", "─" * 10)
    print()
    print("1️⃣  Registration")
    print("2️⃣  Sign in")
    print("3️⃣  Delete Account")
    print("4️⃣  Exit ❌")
    ch = int(input("Enter your choice : "))
    print()
    if ch == 1:
        registration()
    elif ch == 2:
        signin()
    elif ch == 3:
        delacc()
    elif ch == 4:
        exit_program()
    else:
        print("⚠️  Please enter a valid command!")
        menu()


print("*" * 90)
print("*" * 10, "🏦  WELCOME TO BANK ACCOUNT MANAGEMENT SYSTEM  🏦", "*" * 10)
print("*" * 90)
db_connection()
create_database_table()
menu()
