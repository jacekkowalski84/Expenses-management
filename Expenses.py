from csv import DictReader
from dataclasses import dataclass
import pickle
import sys
from typing import Any

import click

FILENAME = r"budget.db"
FILE_CSV = r"expenses.csv"
BIG_EXPANSE_TRESHOLD = 1000

@dataclass
class Expanse:
    id: int
    amount : int
    description: str


    def is_big (self)->bool:
        return self.amount >= BIG_EXPANSE_TRESHOLD


    def __postinit__ (self):
        if self.amount=="":
            raise ValueError ("Missing amount argument!")
        if type(self.amount) != int:
            raise ValueError ("The amount should be an integer!") 
        if self.amount <= 0:
            raise ValueError ("The amount has to be > 0!")
        if self.description == "":
            raise ValueError ("Missing description.")


def open_file ()->list[Expanse]:
    try:
        with open (FILENAME, "rb") as stream:
            expenses = pickle.load (stream)
    except FileNotFoundError:
        expenses = []
    return expenses


def save_file (expanses: list[Expanse])-> None:
    with open (FILENAME, "wb") as stream:
        pickle.dump (expanses, stream)


def id_generate (expenses: list[Expanse])->int:
    all_ids = {expense.id for expense in expenses}
    counter = 0
    while True:
        counter+=1
        if counter not in all_ids:
            new_id = counter
            break
    return new_id


def expanse_item_generate (expenses: list[Expanse], amount_: int, description_: str)-> Expanse:
    return Expanse (
        id = id_generate (expenses),
        amount = int(amount_),
        description = description_
        )


def add_new_expanse (expanses: list[Expanse], amount: int, description: str)-> None:
    try:
        new_expanse = expanse_item_generate (expanses, amount, description)
    except ValueError as e:
        print (f"Error: {e.args[0]}")
    expanses.append (new_expanse)
    save_file (expanses)


def compute_total_expanses (expanses:list[Expanse])->int:
    amounts = [expanse.amount for expanse in expanses]
    amounts_total = sum (amounts)
    return amounts_total


def print_raport (expanses: list[Expanse]) -> None:
    print ("-=ID=- -=AMOUNT=- -=BIG?=- DESCRIPTION")
    if expanses:
        for expanse in expanses:
            if expanse.is_big():
                big = "!"
            else:
                big = ""
            print (f"{expanse.id:^7} {expanse.amount:9} {big:^9} {expanse.description}")
        amounts_total = compute_total_expanses (expanses)
        print (f"  SUM:{amounts_total:11}")
    else:
        print ("Nie wprowadziłeś żadnych wydatków.")


def print_object_raport (expanses: list[Expanse])-> None:
    for expanse in expanses:
        print (f"{expanse!r}")


def open_csv ()->list[dict]:
    try:
        with open (FILE_CSV) as stream:
            reader = DictReader (stream)
            rows = [row for row in reader]
    except FileNotFoundError:
        print ("File not found")
        sys.exit (1)
    return rows


def csv_expanses_import (expanses: list[Expanse], row: dict[str, str])-> None:
    amount = float(row ["amount"])
    description = row ["description"]
    add_new_expanse (expanses, amount, description)



@click.group()
def cli():
    pass

@cli.command()
@click.argument ("amount", type=int)
@click.argument ("description")
def add (amount, description):
    expanses = open_file()
    add_new_expanse (expanses, amount, description)

@cli.command()
def raport()->None:
    expanses = open_file()
    print_raport (expanses)

@cli.command()
def export_python():
    expanses = open_file()
    print_object_raport (expanses)

@cli.command()
def import_csv():
    expanses = open_file()
    reader = open_csv()
    for row in reader:
        csv_expanses_import (expanses, row)
        

if __name__ == "__main__":
    cli()
