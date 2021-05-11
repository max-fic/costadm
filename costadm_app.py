"""
Module Doc String.

"""

from collections import namedtuple
import pandas as pd
from pandas_helper import gen_weighted_func
from costadm_io import write_df

# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name


T_PIS = 0.0165
T_COFINS = 0.0760
Fmt = namedtuple('fmt', ['txt', 'align', 'emp'], defaults=['{}', 'right', 'none'])
ColDesc = namedtuple('colDesc', ['col', 'type', 'fmt'], defaults=[Fmt('{}', 'right', 'none')])

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

    def load_quotes(self, file_name, reader):
        """Doc String."""
        quotes, err = reader(file_name)

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

    def load_prod_vols(self, file_name, reader):
        """Doc String."""
        df, err = reader(file_name)
        if err[0] == 'ok':
            self.df['prod_volumes'] = df
            self.df_valid['prod_volumes'] = True
            self.df_valid['costs_avg'] = False
        return err

    def load_bom(self, file_name, reader):
        """Doc String."""
        df, err = reader(file_name)
        if err[0] == 'ok':
            self.df['structure'] = df
            self.df_valid['structure'] = True
            self.df_valid['costs_item'] = False
            self.df_valid['costs_copacker'] = False
            self.df_valid['costs_avg'] = False
        return err

    def create_bom(self, file_names, reader):
        """Doc String."""
        df, err = reader(file_names)
        print(err)
        if err[0] == 'ok':
            # Update old df with newly read in data frame
            self.df['structure'] = self.bom_update(self.df['structure'], df)
            # set to modified because structure was created from several input files (doent exist yet)
            self.df_valid['structure'] = True
            self.df_modified['structure'] =  True
            self.df_valid['costs_item'] = False
            self.df_valid['costs_copacker'] = False
            self.df_valid['costs_avg'] = False
        return err

    def bom_update(self, df_orig, df_new):
        if df_orig is None or df_orig.empty:
            return df_new
        d1 = df_orig.set_index(['cprod', 'type'])
        d2 = df_new.set_index(['cprod', 'type'])
        ix = d1.index.intersection(d2.index)
        # drop all entries in d1 that also in d2 (d2 overwrites)
        if not ix.empty:
            d1.drop(ix, inplace=True)
        return pd.concat([d1.reset_index(),d2.reset_index()])


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
