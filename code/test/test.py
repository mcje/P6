__author__ = 'Alexander'
" This script is made as a hub to test various things about the reinterpreter "
" We want to tests its limits. What can it do? What is it unable to do?"

import sys
sys.path.append('../')
from framework.case import Case
from framework.predicates import ColumnNotNullPredicate
from framework.predicates import CompareTablePredicate
import  sqlite3
import os

path = "test_program_1.py"

notnull = ColumnNotNullPredicate('Company', 'Name')
compare = CompareTablePredicate('Company', 'Bompany')

input_conn = sqlite3.connect('input1.db')
input2_conn = sqlite3.connect('input2.db')
input3_conn = sqlite3.connect('input3.db')

if os.path.exists('dw.db'):
    os.remove('dw.db')

dw_conn = sqlite3.connect('dw.db')

sales_cur = dw_conn.cursor()

# We make a new table
sales_cur.execute("CREATE TABLE dim1 " +
                  "(key1 INTEGER PRIMARY KEY, attr1 INTEGER, attr2 INTEGER)")

sales_cur.execute("CREATE TABLE dim2 " +
                  "(key2 INTEGER PRIMARY KEY, attr3 INTEGER, attr4 INTEGER)")

sales_cur.execute("CREATE TABLE ft1 " +
                  "(key1 INTEGER PRIMARY KEY)")

# Declaring a program as a string
program = """ __author__ = 'Alexander'

import pygrametl
from pygrametl.datasources import SQLSource
from pygrametl.tables import Dimension, FactTable
import sqlite3

input_conn = sqlite3.connect('input.db')
input2_conn = sqlite3.connect('input2.db')
output_conn = sqlite3.connect('output.db')

input_src = SQLSource(input_conn, query='SELECT * FROM table')
output_wrapper = pygrametl.ConnectionWrapper(connection=output_conn)

dim1 = Dimension(
    'dim1',
    'key1',
    ['attr1', 'attr2']
)

dim2 = Dimension(
    name='dim2',
    key='key2',
    attributes=['attr3', 'attr4']
)

ft1 = FactTable(
    name='ft1',
    keyrefs=['key1']
)

input_conn.close()
output_conn.close()

"""
# Exact amount of sources
Case(path, [input_conn, input2_conn], dw_conn, [notnull, compare], True)

# Too few sources
Case(path, [input_conn], dw_conn, [notnull, compare], True)

# No sources
Case(path, [], dw_conn, [notnull, compare], True)

# Too many sources
Case(path, [input_conn, input2_conn,input3_conn], dw_conn, [notnull, compare], True)

# Wrong dw
Case(path, [input_conn, input2_conn], input3_conn, [notnull, compare], True)

# No predicates
Case(path, [input_conn, input2_conn], dw_conn, [], True)

# 1 predicate
Case(path, [input_conn, input2_conn], input3_conn, [notnull], True)

# Program as string
Case(program, [input_conn, input2_conn], dw_conn, [notnull, compare], False)

# Program as string, but declared as path
Case(program, [input_conn, input2_conn], dw_conn, [notnull, compare], True)

