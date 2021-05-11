# Attention
* xlrd will only read .xls files from version > 1.2 on
* therefore pd.read_excel will report an exception when reading an .xlsx file without specifying the excel reader openpyxl for pandas versions < 1.2.0>

* Default paramenters in functions are bound once. if mutable data type is used and parameter value is changed it stays changed:
````
In [382]: def tst(x=dict(), y=set(), z=[]):
     ...:     print(x, y, z)
     ...:     x[1]=1
     ...:     y.add(1)
     ...:     z.append(1)
     ...: 

In [383]: tst()
{} set() []

In [384]: tst()
{1: 1} {1} [1]
````

<<<<<<< HEAD
#### New Branch for NewAge Integration newage
=======
We have to make sure to unify structure of col_maps_in and to use read_sheet consistently
>>>>>>> branch1
