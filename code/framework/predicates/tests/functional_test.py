from pygrametl.tables import Dimension, SnowflakedDimension
import pygrametl
import os
import sqlite3
from framework.predicates import FunctionalDependencyPredicate
from framework.reinterpreter.datawarehouse_representation import \
    DWRepresentation, DimRepresentation

__author__ = 'Arash Michael Sami Kjær'
__maintainer__ = 'Arash Michael Sami Kjær'

open(os.path.expanduser('func.db'), 'w')

conn = sqlite3.connect('func.db')

cur = conn.cursor()

cur.execute("CREATE TABLE dim1 " +
            "(key1 INTEGER PRIMARY KEY, attr1 INTEGER, key2 INTEGER, "
            "key3 INTEGER)")

cur.execute("CREATE TABLE dim2 " +
            "(key2 INTEGER PRIMARY KEY, attr2 INTEGER, key4 INTEGER)")

cur.execute("CREATE TABLE dim3 " +
            "(key3 INTEGER PRIMARY KEY, attr3 INTEGER)")

cur.execute("CREATE TABLE dim4 " +
            "(key4 INTEGER PRIMARY KEY, attr4 INTEGER)")


data = [
    {'attr1': 3,
     'attr2': 6,
     'attr3': 3,
     'attr4': 9},

    {'attr1': 2,
     'attr2': 8,
     'attr3': 6,
     'attr4': 4},

    {'attr1': 4,
     'attr2': 5,
     'attr3': 3,
     'attr4': 3},

    {'attr1': 1,
     'attr2': 3,
     'attr3': 4,
     'attr4': 4}
]

wrapper = pygrametl.ConnectionWrapper(connection=conn)

dim1 = Dimension(
    name='dim1',
    key='key1',
    attributes=['attr1', 'key2', 'key3'],
    lookupatts=['attr1']
)

dim2 = Dimension(
    name='dim2',
    key='key2',
    attributes=['attr2', 'key4'],
    lookupatts=['attr2']
)

dim3 = Dimension(
    name='dim3',
    key='key3',
    attributes=['attr3']
)

dim4 = Dimension(
    name='dim4',
    key='key4',
    attributes=['attr4']
)

special_snowflake = SnowflakedDimension(references=[(dim1, [dim2, dim3]),
                                                    (dim2, dim4)])

for row in data:
    special_snowflake.insert(row)

conn.commit()

dim1_rep = DimRepresentation(name=dim1.name,
                             key=dim1.key,
                             attributes=dim1.attributes,
                             connection=conn,
                             lookupatts=dim1.lookupatts)

dim2_rep = DimRepresentation(name=dim2.name,
                             key=dim2.key,
                             attributes=dim2.attributes,
                             connection=conn,
                             lookupatts=dim2.lookupatts)

dim3_rep = DimRepresentation(name=dim3.name,
                             key=dim3.key,
                             attributes=dim3.attributes,
                             connection=conn,
                             lookupatts=dim3.lookupatts)

dim4_rep = DimRepresentation(name=dim4.name,
                             key=dim4.key,
                             attributes=dim4.attributes,
                             connection=conn,
                             lookupatts=dim4.lookupatts)

snow_dw_rep = DWRepresentation([dim1_rep, dim2_rep, dim3_rep, dim4_rep],
                               conn, snowflakeddims=(special_snowflake, ))

for dim in snow_dw_rep.dims:
    allatts = dim.all.copy()

    for row in dim.itercolumns(allatts):
        print(dim.name, row)
print('\n')

# writing functional dependencies is an annoying chore
a = ('key3',)
b = ('key1',)
c = (a, b)

d = ('key4',)
e = ('attr2',)
f = (d, e)

g = ('key2',)
h = (d, g)

i = ('attr1',)
j = (i, b)
k = (g, a)
l = (j, k)

# key3 -> key1 | dim1
func_dep1 = FunctionalDependencyPredicate([dim1_rep.name], (c,))
# key4 -> attr2 | dim2
func_dep2 = FunctionalDependencyPredicate([dim2_rep.name], (f,))
# key4 -> key2 | dim2, dim4
func_dep3 = FunctionalDependencyPredicate([dim2_rep.name, dim4_rep.name], (h,))
# key4 -> key2 | dim2
func_dep4 = FunctionalDependencyPredicate([dim2_rep.name], (h,))
# attr1, key1 -> key2, key3 | dim1
func_dep5 = FunctionalDependencyPredicate([dim1_rep.name], l)

print(func_dep1.run(snow_dw_rep))
print(func_dep2.run(snow_dw_rep))
print(func_dep3.run(snow_dw_rep))
print(func_dep4.run(snow_dw_rep))
print(func_dep5.run(snow_dw_rep))

conn.close()