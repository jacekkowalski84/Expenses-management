# **Expense Tracker**
Expense Tracker is a Python application that allows users to effortlessly monitor and manage their expenses by recording them in a SQL database. The program provides the flexibility to choose from multiple relational database management systems (RDBMs) for storing data, including MySQL, SQLite, and PostgreSQL. Additionally, the program's architecture is designed to facilitate easy integration of new RDBMs, enabling support for different databases in the future. With Expense Tracker, budgeting becomes a breeze, giving users an efficient way to track their financial outgoings.

## **Key Features**
-<b>Database and table Creation:</b> If an 'expenses_list' table and/or a database with user given name doesn't exist, the program creates both, exception being PostgreSQL - database has to be created beforehand in this RDBM.

-<b>Expense Addition</b>: The application allows users to add expenses to the database. These expense entries will have specific attributes: id, name, amount, category, and date.

-<b>Expense Reporting</b>: Generates detailed reports based on stored expenses.Generates detailed reports based on stored expenses. Allows users to filter by date or category if necessary arguments are given.


## **Getting Started**
To use the Expense Tracker, follow these steps:

1. **Set up Environment Variables:** Use your preferred code editor (e.g., VSCode) to export the following environment variables:
    
    ```bash
    #For MySQL and PostgreSQL users:
    
    export RDBM='mysql' / 'postgreSQL'
    export HOST='localhost'
    export USER='root'
    export PASSWORD='your_password'
    export DB='your_database'
    
    #For PostgreSQL users:
    
    export RDBM='postgresql'
    export DB='your_database'
    export FILENAME='your_filename'
    
    ```
    
2. **Run Commands:** In the command line, enter 'python' followed by the filepath, then the command argument, and other arguments dependent on the command.

### **Adding an Expense**

To add an expense, follow the command line 'add' argument and 'name', 'amount', 'category', and 'date' arguments. The 'id' argument is automatically assigned by the 'AUTO_INCREMENT' feature in the MySQL database.

Here's an example command to add an expense:
```bash
python expense.py add 'Groceries' 100 'Food' '2022-05-01'
```

### **Generating a Report**

To generate a comprehensive expense report, use the 'report' argument in the command line, like so:
```bash
python expense.py report
```
In addidtion you can add any number of these optional arguments:
- date_min='date'
- date_max='date'
- category='category'
Both "date_min" and "date_max" accept most of the date types.

Here's an example command to create report using all three arguments:
```bash
python expense.py report date_min='Sept 1st 2022' date_max="21.02.2023" category="office_supply"
```

## **Requirements and Dependencies**
The Expense Tracker application requires:

- Python 3.6 or higher

Python modules:
- mysql-connector-python  => 8.0 < 8.1
- psycopg2                => 2.9 < 2.10
- click                   => 8.1 < 8.2

If you haven't installed it, use the following commands:
```bash
pip install mysql-connector-python

pip install psycopg2 

pip install click 
```
