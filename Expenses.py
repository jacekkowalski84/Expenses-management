'''
Usage:
    python Expenses.py <command> <command_parametrs...>

Commands and parameters:
    add <name: str> <amount:float> <category:str> <dat:str>

    raport: no additional parameters

Enviromental variables:
    Note for correct usage enviromental variables for MySQL connection must be set in your terminal:

    export host = 'hostname' (e.g. 'localhost')
    export user = 'username' (e.g. 'root')
    database = 'database_name' (e.g. 'expenses')
    export password = 'password'

'''

from dataclasses import dataclass
from datetime import datetime
import os
import sys

import click
from dateutil import parser
import mysql.connector
from mysql.connector import errorcode


USER= os.environ.get('user')
HOST= os.environ.get('host')
PASSWORD = os.environ.get('password')
DB = os.environ.get('database')
CONFIG = {
        'user': USER,
        'password': PASSWORD,
        'host': HOST,        
        'use_pure': False
        }
CONFIG_DB= {
        'user': USER,
        'password': PASSWORD,
        'host': HOST,   
        'database': DB,     
        'use_pure': False
        }
SQL_QUERIES = {
            'create_database': f'CREATE DATABASE {DB} ',
            'use_database': f'USE {DB}',
            'create_table' : f'''CREATE TABLE {USER}_expenses
                                (
                                exp_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR (30) NOT NULL, 
                                amount DECIMAL(10,2) NOT NULL, 
                                category VARCHAR (15) NOT NULL,
                                date VARCHAR (50) NOT NULL
                                )''',
            'insert' : f'''INSERT INTO {USER}_expenses
                            VALUES
                            (%s, %s, %s, %s, %s)''',
            'select_all' : f'SELECT * FROM {USER}_expenses',
            'select_category': f'category = ',
            'select_date_min': f'date >',
            'select_date_max': f'date <',
                }


class MySQL_Connector:
    def __init__ (self, config):
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()
    

    @classmethod
    def create_database(cls):
        '''Creates 'expenses' database.'''
        connection = mysql.connector.connect(**CONFIG)
        cursor = connection.cursor()
        try:
            cursor.execute(SQL_QUERIES['create_database'])
        except mysql.connector.Error as e:
            raise ValueError (f"Failed creating database: {e}")


    @classmethod
    def use_database (cls)-> None:
        '''Creates an 'expenses' database if one doesn't exists.
        Executes USE 'database' query.'''
        db = cls(CONFIG)
        try:
            db.cursor.execute(SQL_QUERIES['use_database'])
        except mysql.connector.Error as e:
            print(f'Database "{DB}" does not exists.')
            if e.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(db.cursor)
                print (f'Database {DB} created successefully.')            
                db.connection.database = DB
            else:
                raise ValueError (e)
            
    
    @classmethod
    def create_new_table (cls)->None:
        '''Adding new expenses table to database based on username.'''
        db =cls(CONFIG_DB)
        try:
            db.cursor.execute(SQL_QUERIES['create_table'])
            print('Table created.')
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                raise ValueError ("Table with this name already exists.")
            else:
                raise ValueError (e.msg)



@dataclass
class Expanse:
    id: None
    name: str
    amount : float
    category: str
    date: datetime

    def __postinit__ (self):
        if self.id != None:
            raise ValueError ('Expanse ID has to be a None value!')
        if self.name == "":
            raise ValueError ("Missing name.")
        if self.amount=="":
            raise ValueError ("Missing amount argument!")
        if type(self.amount) != int:
            raise ValueError ("The amount should be an integer!") 
        if self.amount <= 0:
            raise ValueError ("The amount has to be > 0!")
    

    def __repr__(self) -> str:
        return f'Expense(id={self.id}, name={self.name!r}, amount={self.amount}, category={self.category}, date={self.date})'


def create_mysql_connection ()-> MySQL_Connector:
    '''Creates a connection to the MySQL server 
    and returns a MySQLConnection object'''
    try:
        connection = MySQL_Connector (CONFIG_DB)
    except mysql.connector.errors.ProgrammingError:
        MySQL_Connector.use_database()
        MySQL_Connector.create_new_table()
        connection = MySQL_Connector(CONFIG_DB)
    return connection

def close_mysql_connection (db: MySQL_Connector)->None:
    db.cursor.close()
    db.connection.close()


def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE {DB} DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as e:
        raise ValueError (f"Failed creating database: {e}")


def create_single_expense (name_:str, amount_: float, category_:str, date_:str)-> Expanse:
    datetype = parser.parse(date_)
    return Expanse (
        id = None,
        name = name_,
        amount = float(amount_),
        category = category_,
        date = datetype
        )


def insert_values (db: MySQL_Connector, expense: Expanse):
    query = SQL_QUERIES ['insert']
    data_expense = (None,
                expense.name,
                expense.amount,
                expense.category,
                expense.date)
    db.cursor.execute(query, data_expense)
    db.connection.commit()
    return db.cursor.fetchall()


def add_apostrophes (text: str)-> str:
    text = f"'{text}'"
    return text

def convert_date_format (text:str)->str:
    try: 
        text_new = parser.parse(text)
        text_new = add_apostrophes (text_new.strftime ("%Y-%m-%d"))
        return text_new
    except:
        raise ValueError ('Wrong date format.')

def generate_raport_query(date_min=None, date_max=None, category=None)->str:
    query = SQL_QUERIES ['select_all']
    counter = 0
    if date_min != None or date_max != None or category != None:
        query = query + ' WHERE '
    if date_min != None:
        date_min = convert_date_format (date_min)
        counter +=1
        query += SQL_QUERIES ['select_date_min'] + date_min
    if date_max != None:
        if counter > 0:
            query += ' AND '
        date_max = convert_date_format (date_max)
        counter +=1
        query += SQL_QUERIES ['select_date_max'] + date_max
    if category != None:
        if counter > 0:
            query += ' AND '
        query += SQL_QUERIES ['select_category'] + add_apostrophes (category)
    query += ';'
    return query


def generate_raport (db: MySQL_Connector, date_min: str, date_max: str, category: str)->None:
    query = generate_raport_query (date_min, date_max, category)
    db.cursor.execute (query)
    print ('-ID- --=NAME=-- -=AMOUNT=- -=CATEGORY=- -=DATE=-')
    for e in db.cursor:
            print (f'{e[0]:3} {e[1]:13} {e[2]:9^} {e[3]:15} {e[4]:12}')

@click.group()
def cli():
    pass
    

@cli.command()
@click.argument ('name')
@click.argument ('amount')
@click.argument ('category')
@click.argument ('date')
def add (name, amount, category, date)->None:
    db = create_mysql_connection()
    try:
        expense = create_single_expense (name, amount, category, date)
        insert_values (db, expense)
    except ValueError as e:
        print (e)
        sys.exit(1)
    close_mysql_connection(db)

@cli.command()
@click.argument ('date_min', required=False)
@click.argument ('date_max', required=False)
@click.argument ('category', required=False)
def raport(date_min:str, date_max:str, category:str)->None:
    db = create_mysql_connection()
    generate_raport(db, date_min, date_max, category)
    close_mysql_connection(db)
       

if __name__ == "__main__":
    cli()

