"""
Module Doc String.

"""

from collections import namedtuple
import pandas as pd
from pandas_helper import gen_weighted_func

# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name


T_PIS = 0.0165
T_COFINS = 0.0760
Fmt = namedtuple('fmt', ['txt', 'align', 'emp'], defaults=['{}', 'right', 'none'])
ColDesc = namedtuple('colDesc', ['col', 'type', 'fmt'], defaults=[Fmt('{}', 'right', 'none')])

map_cols_quotes = {
    'Código': ('citem', 'str'),
    'Descrição': ('item', 'str'),
    'ICMS': ('icms%', 'float'),
    'IPI': ('ipi%',  'float'),
    'Pis/Cofins': ('pis%', 'float'),
    'Preço Convertido R$ c/IPI': ('costtax_item', 'float'),
    'Preço NET s/impostos c/frete': ('cost_item', 'float')
}

map_cols_structure = {
    'Código': ('cprod', 'int'),
    'Produto': ('prod', 'str'),
    'Industrializador': ('ind', 'str'),
    'Tipo de Insumo': ('type', 'str'),
    'Cód. Insumo': ('citem', 'str'),
    'Desc. Insumo': ('item', 'str'),
    'Unidade': ('unit', 'str'),
    'Quantidade': ('quant', 'number'),
    'Perda': ('loss', 'number'),
    # 'Custo': ('cost', 'int'),
}

fmt_cols_structure = {
    'cprod': ('Código', '{:6}'),
    'prod': ('Produto', '{}'),
    'ind': ('Industrializador', '{}'),
    'type': ('Tipo de Insumo', '{}'),
    'citem': ('Cód. Insumo', '{}'),
    'item': ('Desc. Insumo', '{}'),
    'unit': ('Unidade', '{}'),
    'quant': ('Quantidade', '{:9.6f}'),
    'loss': ('Perda', '{:5.2%}'),
    # 'cost': ('Custo', '{:3d}')
}

fmt_cols_quotes = {
    'citem': ('Código', '{}'),
    'item': ('Descrição', '{}'),
    'costtax_item': ('Custo c/ Imp.', '{:6.2f}'),
    'cost_item': ('Custo s/ Imp.', '{:6.2f}'),
    'icms%': ('% ICMS', '{:5.2%}'),
    'ipi%': ('% IPI', '{:5.2%}'),
    'pis%': ('% Pis', '{:5.2%}'),
    'cofins%': ('% Cofins', '{:5.2%}'),
}

map_cols_prod = {
    'CÓD.PROD.': ('cprod', 'int'),
    'NOME_PRODUTO': ('prod', 'str'),
    'Industrializador': ('ind', 'str'),
    'Porcentagem': ('percent', 'number')
}

fmt_cols_prod = {
    'cprod': ('Código', '{:6}'),
    'prod': ('Produto', '{}'),
    'ind': ('Industrializador', '{}'),
    'percent': ('Participação', '{:5.2%}'),
}

type_col = 'type'

sheet_names = {
    'all': 'TOTAL',
    'ME': 'ME',
    'LOG': 'LOG',
    'MP': 'MP',
    'ENV': 'ENV'
}

map_cols_detail = {
    'Matéria-prima': ('item', 'str'),
    'Código New Age': ('citem', 'str'),
    'UND': ('unit', 'str'),
    'Quant': ('quant', 'float'),
    'Perda': ('loss', 'float')
}

fmt_cols_costitem = {
    'cprod': ('Código', '{:6}'),
    'prod': ('Produto', '{}'),
    'ind': ('Industrializador', '{}'),
    'type': ('Tipo de Insumo', '{}'),
    'citem': ('Cód. Insumo', '{}'),
    'item': ('Desc. Insumo', '{}'),
    'unit': ('Unidade', '{}'),
    'quant': ('Quantidade', '{:9.6f}'),
    'loss': ('Perda', '{:5.2%}'),
    'costtax': ('Custo c/ Imp.', '{:7.4f}'),
    'cost': ('Custo s/ Imp.', '{:7.4f}'),
    'ipi%': ('% IPI', '{:5.2%}'),
    'pis%': ('% Pis', '{:5.2%}'),
    'cofins%': ('% Cofins', '{:5.2%}'),
    'icms%': ('% ICMS', '{:5.2%}'),
    'ipi': ('IPI', '{:6.4f}'),
    'pis': ('Pis', '{:6.4f}'),
    'cofins': ('Cofins', '{:6.4f}'),
    'icms': ('ICMS', '{:6.4f}'),
    # 'cost_item': ('Custo Und. s/ Imp.', '{:7.4f}'),
    # 'costtax_item': ('Custo Und. c/ Imp.', '{:7.4f}'),
    # 'costbc':('Custo s/ IPI.', '{:7.4f}')
}

fmt_cols_copacker = {
    'cprod': ('Código', '{:6}'),
    'prod': ('Produto', '{}'),
    'ind': ('Industrializador', '{}'),
    'type': ('Tipo de Insumo', '{}'),
    'costtax': ('Custo c/ Imp.', '{:7.4f}'),
    'cost': ('Custo s/ Imp.', '{:7.4f}'),
    'ipi%': ('% IPI', '{:5.2%}'),
    'pis%': ('% Pis', '{:5.2%}'),
    'cofins%': ('% Cofins', '{:5.2%}'),
    'icms%': ('% ICMS', '{:5.2%}'),
    # 'ipi': ('IPI', '{:6.4%}'),
    # 'pis': ('Pis', '{:6.4%}'),
    # 'cofins': ('Cofins', '{:6.4%}'),
    # 'icms': ('ICMS', '{:6.4%}'),
    # 'ipi': '{:5.4f}',
    # 'pis': '{:5.4f}',
    # 'cofins': '{:5.4f}',
    # 'icms': '{:5.4f}',
    # 'costbc':('Custo s/ IPI.', '{:7.4f}')
}

fmt_cols_avg = {
    'cprod': ('Código', '{:6}'),
    'prod': ('Produto', '{}'),
    'type': ('Tipo de Insumo', '{}'),
    'costtax': ('Custo c/ Imp.', '{:7.4f}'),
    'cost': ('Custo s/ Imp.', '{:7.4f}'),
    'ipi%': ('% IPI', '{:5.2%}'),
    'pis%': ('% Pis', '{:5.2%}'),
    'cofins%': ('% Cofins', '{:5.2%}'),
    'icms%': ('% ICMS', '{:5.2%}'),
    # 'ipi': ('IPI', '{:6.4%}'),
    # 'pis': ('Pis', '{:6.4%}'),
    # 'cofins': ('Cofins', '{:6.4%}'),
    # 'icms': ('ICMS', '{:6.4%}'),
    # 'ipi': '{:5.4f}',
    # 'pis': '{:5.4f}',
    # 'cofins': '{:5.4f}',
    # 'icms': '{:5.4f}',
    # 'costbc':('Custo s/ IPI.', '{:7.4f}')
}

cost_types = [
    'LOG',
    'ME',
    'MP',
    'SERV',
]


# Class with application logic
class CostAdmApp:
    """Doc String."""
    def __init__(self):
        self.df = {
            'structure': None,
            'costs_item': None,
            'costs_copacker': None,
            'costs_avg': None,
            'prod_volumes': None,
            'quotes': None,
        }
        self.df_formats = {
            'structure': fmt_cols_structure,
            'prod_volumes': fmt_cols_prod,
            'quotes': fmt_cols_quotes,
            'costs_item': fmt_cols_costitem,
            'costs_copacker': fmt_cols_copacker,
            'costs_avg': fmt_cols_avg,
        }

        self.grouper = {
            'structure': None,
            'prod_volumes': None,
            'quotes': None,
            'costs_item': None,
            'costs_copacker': self.groupby,
            'costs_avg': self.groupby,
        }

        self.df_group = {
            'structure': None,
            'prod_volumes': None,
            'quotes': None,
            'costs_item': None,
            'costs_copacker': None,
            'costs_avg': ['cprod', 'prod']
        }

        self.df_valid = {
            'structure': False,
            'prod_volumes': False,
            'quotes': False,
            'costs_item': False,
            'costs_copacker': False,
            'costs_avg': False,
        }

        self.df_modified = {
            'structure': False,
            'prod_volumes': False,
            'quotes': False,
            'costs_item': False,
            'costs_copacker': False,
            'costs_avg': False,
        }

        self.sheet_names = {
            'structure': 'Estrutura',
            'prod_volumes': None,
            'quotes': None,
            'costs_item': 'Custos por Item',
            'costs_copacker': 'Custos por Copacker',
            'costs_avg': 'Custos Médios',
        }

    def load_quotes(self, file_name):
        """Doc String."""
        quotes, err = read_sheet(file_name, 'Preços', map_cols_quotes)
        # quotes = quotes.rename(columns=map_cols_quotes)[[c for _, c in map_cols_quotes.items()]]

        if err[0] == 'ok':
            quotes['pis%'], quotes['cofins%'] = \
                        quotes['pis%'] * T_PIS / (T_PIS + T_COFINS), quotes['pis%'] * T_COFINS / (T_PIS + T_COFINS)

            quotes[['ipi%', 'pis%', 'cofins%', 'icms%']] = quotes[['ipi%', 'pis%', 'cofins%', 'icms%']] / 100
            self.df['quotes'] = quotes
            self.df_valid['quotes'], self.df_modified['quotes'] = True, True
            self.df_valid['costs_item'] = False
            self.df_valid['costs_copacker'] = False
            self.df_valid['costs_avg'] = False
        return err

    def load_prod_vols(self, file_name):
        """Doc String."""
        df, err = read_sheet(file_name, 0, map_cols_prod)
        if err[0] == 'ok':
            self.df['prod_volumes'] = df
            self.df_valid['prod_volumes'] = True
            self.df_valid['costs_avg'] = False
        return err

    def load_cost_structure(self, file_name):
        """Doc String."""
        df, err = read_sheet(file_name, 0, map_cols_structure)
        if err[0] == 'ok':
            self.df['structure'] = df
            self.df_valid['structure'] = True
            self.df_valid['costs_item'] = False
            self.df_valid['costs_copacker'] = False
            self.df_valid['costs_avg'] = False
        return err

    def load_recipes(self, file_names):
        """Doc String."""
        df, err = cost_structure_from_recipes(file_names)
        if err[0] == 'ok':
            self.df['structure'] = df
            self.df_valid['structure'], self.df_modified['structure'] = True, True
            self.df_valid['costs_item'] = False
            self.df_valid['costs_copacker'] = False
            self.df_valid['costs_avg'] = False
        return err

    def save(self, types_to_save, file_name):
        """Doc String."""
        # force types_to_save to list
        try:
            _ = types_to_save[0]
        except TypeError:
            types_to_save = [types_to_save]

        # pylint: disable=abstract-class-instantiated
        with pd.ExcelWriter(file_name) as writer:
            for cost_type, sn in self.sheet_names.items():
                if cost_type in types_to_save and sn is not None:
                    print(f'*** save: {cost_type}')
                    if self.df[cost_type] is not None:
                        str_cols = self.df[cost_type].select_dtypes('object').columns
                        print(f'{cost_type}: str_cols = {str_cols}')
                        agg_map = dict()
                        w_sum =  gen_weighted_func('costbc', df=self.df[cost_type], abs=False)
                        agg_cols = set(self.df[cost_type].columns) - set(str_cols)
                        if self.df_group[cost_type] is not None:
                            agg_cols = agg_cols - set(self.df_group[cost_type])
                        for c in agg_cols:
                            agg_map[c] = sum if c not in ['icms%', 'ipi%', 'pis%', 'cofins%'] else w_sum
                        col_map = {col: col_ext for col, (col_ext,_) in self.df_formats[cost_type].items()}
                        write_df(writer, self.df[cost_type], sn, col_map, self.df_group[cost_type], agg_map)
                        #self.df[cost_type][[*col_map]]\
                        #    .reset_index()\
                        #    .rename(columns=col_map)\
                        #    .to_excel(writer, sheet_name=sn, merge_cells=False, index=False)
                        self.df_modified[cost_type] = False

    def calc_costs_item(self):
        """Doc String."""
        if not self.df_valid['structure'] or not self.df_valid['quotes']:
            return
        # pylint: disable=unsubscriptable-object
        costs_item = pd.merge(self.df['structure'],
                              self.df['quotes']
                              [['citem', 'icms%', 'ipi%', 'pis%', 'cofins%', 'costtax_item', 'cost_item']],
                              how='left',
                              on='citem').fillna(0)

        costs_item['cost'] = costs_item['quant'] * (1 + costs_item['loss']) * costs_item['cost_item']
        costs_item['costbc'] =costs_item['cost']\
                              / (1 - costs_item['icms%'] - costs_item['pis%'] - costs_item['cofins%'])
        costs_item['costtax'] = costs_item['quant'] * (1 + costs_item['loss']) * costs_item['costtax_item']
        costs_item['ipi'] = costs_item['costbc'] *  costs_item['ipi%']
        costs_item['pis'] = costs_item['costbc'] *  costs_item['pis%']
        costs_item['cofins'] = costs_item['costbc'] *  costs_item['cofins%']
        costs_item['icms'] = costs_item['costbc'] *  costs_item['icms%']

        self.df['costs_item'] = costs_item
        self.df_valid['costs_item'], self.df_modified['costs_item'] = True, True

    def calc_costs_copacker(self):
        """Doc String."""
        if not self.df_valid['costs_item']:
            print(f'calc_costs_item(): df[costs_item] = {self.df_valid["costs_item"]}')
            return

        cols_category = ['cprod', 'prod', 'ind', 'type']
        cols_val_abs= ['cost', 'costtax', 'costbc', 'ipi', 'pis', 'cofins', 'icms']
        cols_val_rel = ['ipi%','pis%', 'cofins%', 'icms%']
        agg_map = dict()
        for c in cols_val_abs:
            agg_map[c] = sum
        w_sum = gen_weighted_func('costbc', df=self.df['costs_item'], abs=False)
        for c in cols_val_rel:
            agg_map[c] = w_sum

        # Summarize by cprod, prod, ind and type and update tax rates
        # pylint: disable=unsubscriptable-object
        df = self.df['costs_item'][[*cols_category, *cols_val_abs, *cols_val_rel]]\
            .groupby(cols_category) \
            .agg(agg_map)\
            .reset_index()

        self.df['costs_copacker'] = df
        self.df_valid['costs_copacker'], self.df_modified['costs_copacker'] = True, True

    def calc_costs_avg(self):
        """Doc String."""
        if not self.df_valid['costs_item'] or not self.df_valid['prod_volumes']:
            print(f'calc_costs_item(): df[costs_item] = {self.df_valid["costs_item"]},\
                    df[prod_volumes] = {self.df_valid["prod_volumes"]}')
            return

        cols_category = ['cprod', 'prod', 'type']
        cols_val_abs= ['cost', 'costtax', 'costbc', 'ipi', 'pis', 'cofins', 'icms']
        cols_val_rel = ['ipi%','pis%', 'cofins%', 'icms%']
        agg_map = dict()
        for c in cols_val_abs:
            agg_map[c] = sum
        w_sum = gen_weighted_func('costbc', df=self.df['costs_item'], abs=False)
        for c in cols_val_rel:
            agg_map[c] = w_sum

        # Summarize by cprod, prod, ind and type and update tax rates
        # pylint: disable=unsubscriptable-object
        df = self.df['costs_item'][[*cols_category, *cols_val_abs, *cols_val_rel]]\
            .groupby(cols_category) \
            .agg(agg_map)\
            .reset_index()

        self.df['costs_avg'] = df
        self.df_valid['costs_avg'], self.df_modified['costs_avg'] = True, True

    def unsaved_changes(self):
        """Doc String."""
        is_unsaved = False
        for cost_type, valid in self.df_valid.items():
            if valid and cost_type != 'quotes':
                if self.df_modified[cost_type]:
                    is_unsaved = True
        return is_unsaved

    # noinspection PyMethodMayBeStatic
    def groupby(self, df):
        """Doc String."""
        print(f'*** df.groupby: group_cols = {df.columns}')
        group_cols = list({'cprod', 'prod', 'ind'} & set(df.columns))
        print(f'*** df.groupby: group_cols = {group_cols}')
        ### QUICK HACK
        val_cols = set(df.columns) - set(group_cols)
        cols_val_rel = set(['ipi%','pis%', 'cofins%', 'icms%']) & val_cols
        cols_val_abs = val_cols - set(cols_val_rel)
        str_cols = df.select_dtypes('object').columns
        agg_map = dict()
        for c in set(cols_val_abs) -  set(str_cols):
            agg_map[c] = sum

        ### QUICK HACK
        w_sum = gen_weighted_func('costbc', df=df, abs=False)
        for c in cols_val_rel:
            agg_map[c] = w_sum
        print(f'*** groupby: agg_map = {agg_map}')
        if group_cols:
            df = df.groupby(group_cols).agg(agg_map).reset_index()
        return df


# Helper Functions

def gen_cost_structure(df, cprod, prod, ind, cost_type, factor):
    """Doc String."""
    total = df.loc[df['item'] == 'Total', 'quant'].iloc[0]
    df = df.dropna(subset=['citem'])  # drops the Total line as well
    lng = df.shape[0]
    df_cols = dict()

    df_cols['cprod'] = [cprod] * lng
    df_cols['prod'] = [prod] * lng
    df_cols['ind'] = [ind] * lng
    df_cols['type'] = [cost_type] * lng
    for c in {_c for _c in df.columns}:
        df_cols[c] = df[c]
    # df_cols['cost'] = [0] * lng
    df_cols['quant'] = df_cols['quant'] / total * factor  # scale to one unit

    return pd.DataFrame(df_cols)


def read_excel(file_name, *args, **kwargs):
    """Doc String."""
    df = None
    ret = ('ok',None)
    try:
        df = pd.read_excel(file_name, *args, **kwargs)
    # pylint: disable=broad-except
    except Exception as err:
        print(f"*** read_excel Type(err) = {type(err)}, hasattr(err,'args') = {hasattr(err, 'args')}")
        print(f'*** read_excel: Error: {err.args[0]}')
        ret =  ('file_not_found', err.args[0] if len(err.args) > 0 else "Unidentified Error")
    return df, ret


def read_sheet(file, sn, map_cols_new, max_rows=10, **kwargs):
    """Doc String."""

    col_names = [c for c in map_cols_new]  # create a list in case map_cols_new is a dict
    df, err = read_excel(file, sheet_name=sn, header=None, nrows=max_rows)
    if err[0] != 'ok':
        print(f'*** read_excel: Error: {err}')
        return df, err

    row, cols_not_found  = pos_colnames(df, col_names, max_rows)

    print(f'*** read_sheet: file ={file}, row ={row}, cols_not_found = {cols_not_found}')
    if row < 0:
        return None, ('cols_not_found', f"Couldn't find columns {cols_not_found}!")

    # read again from the correct satarting position (will have correct col names adn dtypes)
    df, err = read_excel(file, sheet_name=sn, skiprows=row, usecols=col_names, **kwargs)
    if err[0] != 'ok':
        return df, err

    if isinstance(map_cols_new, dict):
        # create mappings
        map_rename, dtype_cols = dict(), dict()
        for col_old, (col_new, dtype_col) in map_cols_new.items():
            map_rename[col_old] = col_new
            dtype_cols[dtype_col] = [*dtype_cols.get(dtype_col, []), col_old]
        ret = check_dtypes(df, dtype_cols)
        if ret[0] != 'ok':            # if not empty dict -> columns with wrong dt found
            err = ('wrong_dtype', ret[1])
            print(f'*** read_sheet: {err}')
            return None, err

        df = df.rename(columns=map_rename)

    return df, ('ok', None)


def pos_colnames(df, col_names, max_rows=0):
    """Doc String."""
    row = -1
    cols_to_find = len(col_names)
    df_rows, df_cols = df.shape
    max_rows = max_rows if max_rows > 0 else df_rows
    cols_not_found = col_names[:]
    for i in range(0, max_rows):
        n_found = 0
        for j in range(0, df_cols):
            if df.iat[i, j] in col_names:
                # map column name from pd.read_excel (which is a number corr to nth column) to new column name
                cols_not_found.remove(df.iat[i, j])
                n_found += 1
                if n_found == cols_to_find:
                    break
        if n_found == cols_to_find:
            row = i
            break
    return row, cols_not_found


def cost_structure_from_recipes(files):
    """Doc String."""
    df_list = []

    for file in files:
        print(f'Processing file {file}')
        sh_index, err = read_sheet(file, 'Index', ['cprod', 'prod', 'ind', 'type', 'detail', 'fator'])
        if err[0] != 'ok':
            return None, err

        # Process all items in index
        sh_index = sh_index.dropna(subset=['detail'])
        for cprod, prod, ind, cost_type, detail, factor in zip(sh_index['cprod'], sh_index['prod'], sh_index['ind'],
                                                               sh_index['type'], sh_index['detail'], sh_index['fator']):
            df, err = read_sheet(file, detail, map_cols_detail)
            if err[0] != 'ok':
                return None, err
            # print(f'Appending {cprod}, {prod}, ind, {cost_type}')
            df_list.append(gen_cost_structure(df, cprod, prod, ind, cost_type, factor))

    return pd.concat(df_list, ignore_index=True), ('ok',None)


def check_dtypes(df, dtype_cols):
    """Doc String."""
    wrong_dt = dict()
    for dt, cols in dtype_cols.items():
        dt = 'object' if dt == 'str' else dt
        df_cols = df.select_dtypes(dt).columns
        cols_wrong_dt = set(cols) - set(df_cols)
        if cols_wrong_dt:
            wrong_dt[dt] = cols_wrong_dt

    if wrong_dt != {}:
        return 'wrong dtype', f'Wrong data type, expected: {wrong_dt.__str__()[1:-1]}'
    else:
        return 'ok', None

def write_df(xls_writer, df, sn, col_map, cols_group, agg_map):
    """Doc String."""
    print(f'*** write_df: {sn}')
    print(df.columns)
    print(col_map)
    if cols_group:
        for c in cols_group:
            print(f'*** cols_group = {c}')
        for c in agg_map:
            print(f'*** agg_map[{c}] ={agg_map[c]}')
        df = df.groupby(cols_group).agg(agg_map).reset_index()
        print(f'*** after group {df.columns}')

    # sort columns to write according to format order
    sort_key_func = lambda x : {k:i for i, k in enumerate(col_map)}[x]
    cols_write = [col_map[i] for i in sorted(list(set(df.columns) & set(col_map)),key=sort_key_func)]
    print(f'col_map = {[*col_map]}')
    print(f'cols_write = {cols_write}')
    df.rename(columns=col_map)[cols_write]\
                  .to_excel(xls_writer, sheet_name=sn, merge_cells=False, index=False)

if __name__ == '__main__':
    f = '/Users/maxi/Documents/WOW/CUSTOS/ABR/Itens Embalagens.xlsx'
    sh = 'LITRO BC'

    df = cost_structure_from_recipes([f])
    print(df)
