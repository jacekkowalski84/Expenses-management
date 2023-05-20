"""
Usage:
pytest commit_5\tests\test_Expenses.py
"""
import pytest
import psycopg2
from unittest.mock import patch

import expense_tracker.SQL_Connectors as SQL_Connectors
import expense_tracker.Expenses as Expenses

### TESTING MYSQL CONNECTION

def check_mysql_connection():
    try:
        conn = SQL_Connectors.MySQL_Connector (Expenses.MYSQL_CONFIG_DB)
        return False
    except ValueError:
        return True

@pytest.mark.parametrize('rdbm, expected_connector', 
                         [
                        ('mysql', SQL_Connectors.MySQL_Connector),
                        ])
@patch('os.environ.get')
@pytest.mark.skipif (check_mysql_connection(), reason= "MySQL database doesn't exist")
def test_init_connection(mock_get, rdbm, expected_connector):
    mock_get.return_value = rdbm
    connector = Expenses.init_connection(rdbm)
    assert isinstance(connector, expected_connector)

### TESTING POSTGRESQL CONNECTION

def check_postgre_connection():
    try:
        conn = SQL_Connectors.PostgreSQL_Connector (Expenses.HOST, Expenses.DB, Expenses.USER, Expenses.PASSWORD)
        return False
    except ValueError:
        return True


def create_test_database_postgre():
    '''Creates virtual PostgreSQL database for test purposes'''
    config = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'mysecretpassword',
        'database': 'postgres'  
    }
    conn = psycopg2.connect(**config)
    conn.autocommit = True
    cursor = conn.cursor()
    test_database = 'test_database'
    cursor.execute(f"CREATE DATABASE {test_database}")
    cursor.close()
    conn.close()
    config['database'] = test_database
    return config


@pytest.fixture(scope='session')
def test_database_postgre():
    conn_params = create_test_database_postgre()
    yield conn_params
    conn = psycopg2.connect(**conn_params)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE {conn_params['database']}")
    cursor.close()
    conn.close()


@pytest.mark.parametrize('rdbm, expected_connector', 
                         [
                        ('postgresql', SQL_Connectors.PostgreSQL_Connector),
                        ])
@patch('os.environ.get')
@pytest.mark.skipif (check_postgre_connection(), reason= "PostgreSQL database doesn't exist")
def test_init_connection_postgre(mock_get, rdbm: str, expected_connector, test_database_postgre: dict):
    '''This test will execute only if PostgreSQL RDBM is selected and valid enviromental arguments for Postgre connection are given.'''
    mock_get.return_value = rdbm
    connector = Expenses.init_connection(rdbm)
    assert isinstance(connector, expected_connector)


###TESTING SQLITE CONNECTION

def check_sqlite_connection():
    try:
        conn = SQL_Connectors.SQLite_Connector(Expenses.FILENAME)
        return False
    except ValueError:
        return True

@pytest.mark.parametrize('rdbm, expected_connector', [
    ('sqlite', SQL_Connectors.SQLite_Connector),
])
@patch('os.environ.get')
@pytest.mark.skipif(check_sqlite_connection(), reason="SQLite database doesn't exist")
def test_init_connection(mock_get, rdbm, expected_connector):
    mock_get.return_value = rdbm
    connector = Expenses.init_connection(rdbm)
    assert isinstance(connector, expected_connector)


@patch('os.environ.get')
def test_init_connection_invalid_rdbm(mock_get):
    mock_get.return_value = None
    with pytest.raises(ValueError):
        Expenses.init_connection('invalid_rdbm')


###OTHER TESTS


def test_new_expense():
    got = Expenses.create_single_expense ('movie_tickets', 64.50, 'entertainment', 'Jan 3rd 2023')
    expected = Expenses.Expanse (None, 'movie_tickets', 64.50, 'entertainment', Expenses.datetime(2023, 1, 3, 0, 0))
    assert got == expected


def test_parse_date():
    got= Expenses.convert_date_format('4th June 2021')
    expected = "'2021-06-04'"
    assert got == expected


def test_report_query_1():
    got = Expenses.generate_report_query(None, None, None)
    expected = f'SELECT * FROM expenses_list;'
    assert got == expected

def test_report_query_2():
    got = Expenses.generate_report_query('jan 5th 2022', None, None)
    expected = f"SELECT * FROM expenses_list WHERE date >'2022-01-05';"
    assert got == expected

def test_report_query_3():
    got = Expenses.generate_report_query('jan 5th 2022', '14.04.2023', None)
    expected = f"SELECT * FROM expenses_list WHERE date >'2022-01-05' AND date <'2023-04-14';"
    assert got == expected

def test_report_query_4():
    got = Expenses.generate_report_query('jan 5th 2022', '14.04.2023', 'entertainment')
    expected = f"SELECT * FROM expenses_list WHERE date >'2022-01-05' AND date <'2023-04-14' AND category = 'entertainment';"
    assert got == expected