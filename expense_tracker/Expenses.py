'''
Usage:
    python Expenses.py <command> <command_parametrs...>

Commands and parameters:
    add <name: str> <amount:float> <category:str> <date:str>

    report: (Optional: category)

Enviromental variables:
    Note for correct usage enviromental variables for MySQL connection must be set in your terminal:

    export RDBM='rdbm_name' (e.g. 'mysql', 'postgresql', 'sqlite')
    export HOST='hostname' (e.g. 'localhost')
    export USER='username' (e.g. 'root')
    export DATABASE='database_name' (e.g. 'expenses')
    export PASSWORD='password'
    export FILENAME='filename' (only for SQLite)

'''

from dataclasses import dataclass
from datetime import datetime
import os
import sys

import click
from dateutil import parser

from SQL_Connectors import Connector, MySQL_Connector, PostgreSQL_Connector, SQLite_Connector


###    ENVIROMENTAL ARGUMENTS   ###
RDBM = os.environ.get('RDBM')
USER= os.environ.get('USER')
HOST= os.environ.get('HOST')
PASSWORD = os.environ.get('PASSWORD')
DB = os.environ.get('DB')
FILENAME = os.environ.get('FILENAME')
MYSQL_CONFIG = {
        'user': USER,
        'password': PASSWORD,
        'host': HOST,        
        'use_pure': False
        }
MYSQL_CONFIG_DB= {
        'user': USER,
        'password': PASSWORD,
        'host': HOST,   
        'database': DB,     
        'use_pure': False
        }


######     SQL QUERIES:    ######

Q_CREATE_DATABASE = f'CREATE DATABASE {DB} '
Q_INSERT_VALUE = '''INSERT INTO expenses_list
                    VALUES (%s, %s, %s, %s, %s);'''
Q_SELECT_ALL = 'SELECT * FROM expenses_list'
Q_SELECT_BY_CATEGORY = 'category = %s'
Q_DATE_MIN = 'date >'
Q_DATE_MAX = 'date <'


@dataclass
class Expanse:
    id: None | int
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


def init_connection(rdbm: str|None) -> Connector:
    if rdbm == 'mysql':
        return MySQL_Connector(MYSQL_CONFIG_DB)
    elif rdbm == 'sqlite':
        return SQLite_Connector(FILENAME)
    elif rdbm == 'postgresql':
        return PostgreSQL_Connector(HOST, DB, USER, PASSWORD)
    else:
        raise ValueError(f'{RDBM} is an incorrect RDBM choice.')


def init_database (conn: Connector)->None:
    conn.create_database (MYSQL_CONFIG, Q_CREATE_DATABASE)


def init_table (conn: Connector)->None:
    conn.create_table()


def close_connection(conn: Connector)->None:
    conn.connection.close()
    conn.sqlcursor.close()


def create_single_expense (name_:str, amount_: float, category_:str, date_:str)-> Expanse:
    datetype = parser.parse(date_)
    return Expanse (
        id = None,
        name = name_,
        amount = float(amount_),
        category = category_,
        date = datetype
        )


def insert_values (db: Connector, expense: Expanse):
    query = Q_INSERT_VALUE
    data_expense = (None,
                expense.name,
                expense.amount,
                expense.category,
                expense.date)
    db.sqlcursor.execute(query, data_expense)
    db.connection.commit()
    return db.sqlcursor.fetchall()


def add_apostrophes (text: str)-> str:
    text = f"'{text}'"
    return text

def convert_date_format (text:str)->str:
    '''Converts given date format into format accepted by SQL databse'''
    try: 
        text_new = parser.parse(text)
        text_new = add_apostrophes (text_new.strftime ("%Y-%m-%d"))
        return text_new
    except:
        raise ValueError ('Wrong date format.')

def generate_report_query(date_min: str|None = None, date_max: str|None = None, category: str|None = None)->str:
    '''Generates a query for creating a report based on the number of optional arguments given'''
    query = Q_SELECT_ALL
    counter = 0
    if date_min != None or date_max != None or category != None:
        query = query + ' WHERE '
    if date_min != None:
        date_min = convert_date_format (date_min)
        counter +=1
        query += Q_DATE_MIN + date_min
    if date_max != None:
        if counter > 0:
            query += ' AND '
        date_max = convert_date_format (date_max)
        counter +=1
        query += Q_DATE_MAX + date_max
    if category != None:
        if counter > 0:
            query += ' AND '
        query += Q_SELECT_BY_CATEGORY + add_apostrophes(category)
    query += ';'
    return query


def generate_report (conn: Connector, date_min: str|None = None, date_max: str|None = None, category: str|None = None)->None:
    query = generate_report_query (date_min, date_max, category)
    report = conn.cursor_execute(query)
    print ('-ID- --=NAME=-- -=AMOUNT=- -=CATEGORY=- -=DATE=-')
    for element in report:
            print (f'{element[0]:3} {element[1]:13} {element[2]:9^} {element[3]:15} {element[4]:12}')

@click.group()
def cli():
    pass
    
@cli.command()
def create_database ()->None:
    if RDBM == 'mysql':
        conn = MySQL_Connector(MYSQL_CONFIG)
    else:
        conn = init_connection(RDBM)
    try:
        init_database(conn)
        close_connection(conn)
    except ValueError as e:
        print (e)
    try: 
        conn = init_connection(RDBM)
        init_table (conn) 
        close_connection (conn)
    except ValueError as e:
        print (e)
    
    

@cli.command()
@click.argument ('name')
@click.argument ('amount')
@click.argument ('category')
@click.argument ('date')
def add (name: str, amount: float, category: str, date: str)->None:
    conn = init_connection(RDBM)
    try:
        expense = create_single_expense (name, amount, category, date)
        insert_values (conn, expense)
    except ValueError as e:
        print (e)
        sys.exit(1)
    close_connection (conn)


@cli.command()
@click.argument ('date_min', required=False)
@click.argument ('date_max', required=False)
@click.argument ('category', required=False)
def report(date_min:str, date_max:str, category:str)->None:
    conn = init_connection(RDBM)
    generate_report(conn, date_min, date_max, category)
    close_connection (conn)
       

if __name__ == "__main__":
    cli()

