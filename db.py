import os
import pandas as pd

class DB:
    def __init__(self, db_io):
        self.db_io = db_io.open()

    def open(self):
        return self.db_io.open()

    def close(self):
        return self.db_io.close()

    def write(self, table, df):
        if isinstance(table, str):
            return self.db_io.write(table, df) 
        dfs = dict()
        dfs = { t: self.db_io.write(table, df[table]) for t in table }
        return dfs

    def read(self, table):
        if isinstance(table, str):
            return self.db_io.read(table) 
        dfs = dict()
        dfs = { t: self.db_io.read(table) for t in table }
        return dfs

    def __getattr__(self, *args, **kwargs):
        return(self.db_io.__getattr__(*args, **kwargs))

class XlsDB:
    def __init__(self, wbook, user_info=None):
        assert(os.path.isfile(wbook))
        self.wbook = wbook
        self.user_info = user_info
        self.table = dict()
        self.name = set()
        self.status = dict()
        self.is_open = False

    def open(self):
        if self.is_open:
            print(f'*** open(): Already Open!')
            return
        self.name = set( t for t in pd.read_excel(self.wbook, sheet_name=None, nrows=0))
        self.status = { t: 'void'  for t in self.name }    # status: void, read, write
        self.is_open = True
        return self

    def close(self):
        if not self.is_open:
            return self

        with pd.ExcelWriter(self.wbook) as writer:
            for t in self.table:
                if self.status[t] != 'write':
                    continue
                print(f'*** close(): Modified = {self.status[t]}, Writing {t}')
                self.table[t].to_excel(writer, t, index=False, merge_cells=False)
        self.is_open = False
        return self
        
    def write(self, table, df):
        assert(df is not None)
        assert(self.is_open)
        assert(table in self.name)
        self.table[table] = df.copy()
        self.status[table] = 'write'
        return df
        
    def read(self, table):
        assert(self.is_open)
        assert(table in self.name)

        if self.status[table] == 'void':
            self.table[table] = pd.read_excel(self.wbook, table)
            self.status[table] = 'read'

        return self.table[table].copy()

    def new(self, table, df):
        assert(df is not None)
        assert(self.is_open)
        assert(table not in self.name)
        self.table[table] = df.copy()
        self.status[table] = 'write'
        self.name.add(table)
        return df