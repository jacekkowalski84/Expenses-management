import mysql.connector
import psycopg2
import sqlite3


class Connector:
    """
    Base class for SQL connectors.
    """

    def cursor_execute(self, query: str, values=None):
        """
        Executes the given SQL query with the given parameter values.
        """
        if values is None:
            values = ()
        self.sqlcursor.execute(query, values)
        if values != ():
            self.connection.commit()
        return self.sqlcursor.fetchall()


class MySQL_Connector (Connector):
    def __init__ (self, config: dict[str, str])->None:
        """
        Creates a new connection to a MySQL database.
        """
        try:
            self.connection = mysql.connector.connect(**config)
            self.sqlcursor = self.connection.cursor()
        except mysql.connector.Error as e:
            raise ValueError(f"Failed to connect to database: {e}")
    

    @classmethod
    def create_database(cls, config: dict [str, str], query: str)->None:
        '''Creates a new database in a MySQL server.'''
        connection = mysql.connector.connect(**config)
        sqlcursor = connection.cursor()
        try:
            sqlcursor.execute (query)
            print ('Database "expenses" created.')
            connection.close()
            sqlcursor.close()
        except mysql.connector.Error as e:
            raise ValueError(f"Failed creating database: {e}")
    
    
    def create_table(self, table_desc: str)->None:
        '''Creates a table in a MySQL server.'''
        query = f'CREATE TABLE {table_desc}'
        try:
            self.cursor_execute(query)
            print ('Table created.')
        except mysql.connector.Error as e:
            raise ValueError(f"Failed creating table: {e}")
             

class PostgreSQL_Connector (Connector):
    def __init__(self, host: str|None, db: str|None, user: str|None, password: str|None)->None:
        """
        Creates a new connection to a PostgreSQL database.
        """
        try:
            self.connection = psycopg2.connect(
                host=host,
                database=db,
                user=user,
                password=password
            )
            self.sqlcursor = self.connection.cursor()
        except psycopg2.Error as e:
            raise ValueError(f"Failed to connect to database: {e}")


    @classmethod
    def create_database(cls, config: dict [str, str], query: str)->None:
        """
        psycopg2 does not support 'CREATE DATABASE' query. 
        You need to have the database already created in the PostgreSQL server 
        before connecting to it using psycopg2.
        """
        raise ValueError ('Database with this name does not exist. Please log in to PostgreSQL client and create a database.')
    
    
    def create_table(self, table_desc)->None:
        '''Creates a table in a PostgreSQL server.'''
        query = f'CREATE TABLE {table_desc}'
        try:
            self.cursor_execute(query)
            print ('Table created.')
        except mysql.connector.Error as e:
            raise ValueError(f"Failed creating table: {e}")

    
class SQLite_Connector (Connector):
    def __init__(self, db):
        """
        Creates a new connection to a SQLite database.
        """
        self.connection = sqlite3.connect(db)
        self.sqlcursor = self.connection.cursor()


    def cursor_execute(self, query: str, values: tuple = ()):
        query_new = query.replace(r'%s', '?')
        return super().cursor_execute(query_new, values)


    @classmethod
    def create_database(cls, config: dict [str, str], query: str)->None:
        """
        Does nothing because creating a database is not necessary in SQLite.
        """
        pass

    
    def create_table(self, table_desc)->None:
        '''Creates a table in a MySQL server.'''
        query = f'CREATE TABLE IF NOT EXIST {table_desc}'
        try:
            self.cursor_execute(query)
            print ('Table created.')
        except mysql.connector.Error as e:
            raise ValueError(f"Failed creating table: {e}")





