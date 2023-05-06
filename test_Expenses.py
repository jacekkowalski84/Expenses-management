"""
Usage:
pytest test_Expenses.py
"""

from Expenses import generate_raport_query, USER


def test_raport_query_1():
    got = generate_raport_query(None, None, None)
    expected = f'SELECT * FROM {USER}_expenses;'
    assert got == expected

def test_raport_query_2():
    got = generate_raport_query('jan 5th 2022', None, None)
    expected = f"SELECT * FROM root_expenses WHERE date >'2022-01-05';"
    assert got == expected

def test_raport_query_3():
    got = generate_raport_query('jan 5th 2022', '14.04.2023', None)
    expected = f"SELECT * FROM root_expenses WHERE date >'2022-01-05' AND date <'2023-04-14';"
    assert got == expected

def test_raport_query_4():
    got = generate_raport_query('jan 5th 2022', '14.04.2023', 'entertainment')
    expected = f"SELECT * FROM root_expenses WHERE date >'2022-01-05' AND date <'2023-04-14' AND category = 'entertainment';"
    assert got == expected