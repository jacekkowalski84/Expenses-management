# Expense Tracker
A Python program that allows you to track your expenses by adding them to a MySQL database.

# Features
-Creates a new MySQL database named expenses if it doesn't already exist.

-Creates a new expenses table with the name of the user.

-Adds expenses to the database with the following attributes: id, name, amount, category, and date.

-Generates a report of all expenses in the database.

# Usage
Using one's preferred code editor (e.g. VSCode):

-Export the environment variables host, user, password_to_db, and database with your MySQL connection information. For example

```bash
export host='localhost'

export user='root'

export password_to_db='your_password'

export database='your_database'
```


- Enter keyword 'python' followed by filepath then the command argument and other arguments dependent on command.


# Adding an Expense
To add an expense, follow the command line by 'add' argument and 'name', 'amount', 'category', and 'date' arguments. 
The 'id' argument is set to None, since id is being assigned by 'AUTO_INCREMENT' option i MySQL database.

For example:
```bash
python expense.py add 'Groceries' 100 'Food' '2022-05-01'
```

# Generating a Report
To generate a report of all expenses in the database, follow the command line by 'report' argument.

For example:
```bash
python expense.py report
```

# Code and Resources Used
Python 3.6 or higher

mysql-connector-python library (you can install it with pip install mysql-connector-python)
