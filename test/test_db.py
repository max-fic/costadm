from os import path
import pytest
import pandas as pd
from db import XlsDB

@pytest.fixture
def gen_db(tmpdir):
    df = pd.DataFrame({'a': ['1', '2'], 'b':[2,4,]})
    db_name = path.join(tmpdir, 'tst.xlsx')
    db_name_orig = path.join(tmpdir, 'tst_orig.xlsx') 
    table = 'tst'
    df.to_excel(db_name, table, index=False, merge_cells=False)
    df.to_excel(db_name_orig, table, index=False, merge_cells=False)
    return db_name, db_name_orig, table

def test_init_1(gen_db):
    db_name, _, _ = gen_db
    db = XlsDB(db_name)
    assert db is not None

def test_init_2(gen_db):
    db_name, _, _ = gen_db
    with pytest.raises(AssertionError):
        dir= path.dirname(db_name)
        db = XlsDB(path.join(dir, 'dummy.xlsx'))


def test_open(gen_db):
   db_name, _, table = gen_db 
   print(table)
   db = XlsDB(db_name)
   db.open()
   assert db.is_open
   assert db.name == set([table])
   assert db.status[table] == 'void'


def test_read_1(gen_db):
   db_name, _, table = gen_db 
   db = XlsDB(db_name)
   db.open()
   with pytest.raises(AssertionError):
       df = db.read(table[:-1])


def test_read_2(gen_db):
   db_name, _, table = gen_db 
   db = XlsDB(db_name)
   db.open()
   df = db.read(table)
   assert db.status[table] == 'read'
   assert df.iloc[0,1] == 2


def test_write_1(gen_db):
   db_name, _, table = gen_db 
   db = XlsDB(db_name)
   db.open()
   df = pd.DataFrame({'a':[1, 2], 'b':[3, 4]})
   with pytest.raises(AssertionError):
        db.write(table[:-1], df)


def test_write_2(gen_db):
   db_name, _, table = gen_db 
   db = XlsDB(db_name)
   db.open()
   df = None
   with pytest.raises(AssertionError):
        db.write(table, df)


def test_write_3(gen_db):
   db_name, _, table = gen_db 
   db = XlsDB(db_name)
   db.open()
   df = pd.DataFrame({'a':[1, 2], 'b':[3, 4]})
   db.write(table, df)
   df = db.read(table)
   assert db.status[table] == 'write'
   assert df.iloc[0,1] == 3


def test_write_1(gen_db):
   db_name, _, table = gen_db 
   db = XlsDB(db_name)
   db.open()
   df = db.read(table)
   assert db.status[table] == 'read'
   assert df.iloc[0,1] == 2



def test_close_1(gen_db):
   db_name, _, table = gen_db 
   db = XlsDB(db_name)
   db.open()
   df = pd.DataFrame({'a':[1, 2], 'b':[3, 4]})
   db.write(table, df)
   db.close()
   df = pd.read_excel(db_name,table)
   assert df.iloc[0,1] == 3 


def test_new_1(gen_db):
   db_name, _, table = gen_db 
   table_new = table + '_new'
   db = XlsDB(db_name)
   db.open()
   df = pd.DataFrame({'a':[1, 2], 'b':[3, 4]})
   db.new(table_new, df)
   assert db.status[table_new] == 'write'
   assert db.name == set([table, table_new])
   df = db.read(table_new)
   assert df.iloc[0,1] == 3  