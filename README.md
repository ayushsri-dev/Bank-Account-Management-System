# 🏦 Bank Account Management System

This project is a console-based application built in **Python** for managing basic bank account operations, utilizing **MySQL** for data persistence. It demonstrates essential full-stack workflow concepts including user registration, data validation, and basic account management features.

## ✨ Features

  * **User Registration:** Allows users to register and automatically generates a unique 8-digit **Account Number**.
  * **Sign-In:** Secure login using Name and Account Number.
  * **KYC Management:** Users can update their profile (Name, Age, Phone, Email) and link their Aadhaar number.
  * **PIN Management:** Change account PIN with a simulated **OTP confirmation** flow for security.
  * **Account Transfer/Deletion:** Functionality to transfer account ownership or delete the account entirely (both require OTP confirmation).
  * **Database Setup:** Automatically creates the `Bank_Account_Management` database and the required `Profile` and `Account` tables on the first run.

## 🛠️ Prerequisites

To run this application, you need the following:

1.  **Python 3.x**

2.  **MySQL Server:** Ensure your MySQL service is running locally.

3.  **Python Connector:** You must install the MySQL Python connector library:

    ```bash
    pip install mysql-connector-python
    ```

## ⚙️ Setup and Configuration

### 1\. Database Credentials

The application connects to MySQL using hardcoded credentials in the `db_connection()` function. You **must** update this line in `Source_Code.py` to match your local MySQL configuration:

```python
def db_connection():
    global con, cursor
    try:
        # UPDATE the 'passwd' here to your MySQL root password!
        con = mysql.connector.connect(host='localhost', user='root', passwd='tiger') 
        cursor = con.cursor()
    # ...
```

### 2\. Running the Application

After updating the credentials, run the program from your terminal:

```bash
python Source_Code.py
```

The system will connect to the database, ensure the necessary tables exist, and present the main menu.

## ⚠️ Security Note (For Educational Use)

This project is intended as a learning tool to demonstrate database interaction. It contains a critical security vulnerability: **the account PIN is stored in plaintext** within the `Account` table.

*In a real-world application, sensitive data like PINs and passwords must always be stored as securely hashed values (using libraries like `bcrypt` or `hashlib`) and never in plaintext.*

## 📂 Project Structure

```
.
├── Source_Code.py      # Main application logic and database interactions
└── README.md           # Project documentation (this file)
```
