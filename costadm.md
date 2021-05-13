# Attention
* xlrd will only read .xls files from version > 1.2 on
* therefore pd.read_excel will report an exception when reading an .xlsx file without specifying the excel reader openpyxl for pandas versions < 1.2.0>

* Default paramenters in functions are bound once. if mutable data type is used and parameter value is changed it stays changed:
````python
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

### testing
Comamand palette: `CMD+Shift+P` or `View->Command Palette`
How to set parameters manually in `vscode`:
Command Palette: `Open Settings (JSON)`

In settings.json:
````json
"python.testing.pytestEnabled": true
"python.testing.pytestPath": "<test-dir>"
````
Set up a testdirectory with the test scripts `test-dir`

Running tests:`CMD+Shift+P` [Run all tests]

`pytest`:

Define fixture
````python
Setting fixtures: set up routines
@pytest.fixture
def my_fixture():
    ...
````
Then define the test function with a parameter named `my_fixture`

````python
def my_test(my_fixture)
    ...
````
`my_test` will be run with the result of `my_fixture`.


Stacking a data frame from horizontal to vertical:
````python
df.melt(id_vars=[Varsi, that, wont, be, stacked], 
        value_vars=[Names, of, stackable, columns], 
        var_name='Criteria Col',
        value_var='Value Col')
````
