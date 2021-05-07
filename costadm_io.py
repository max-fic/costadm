# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name
# pylint: disable=fixme

import os
import pandas as pd

wbooks = [
    '08.04.2021 -  Sufresh Bebida Abacaxi.xlsx',
    '08.04.2021 -  Sufresh Bebida Manga.xlsx',
    '22.04.2021 -  Sufresh Bebida Laranja.xlsx',
    '23.04.2021 -  Sufresh Bebida Pessego.xlsx',
    '24.04.2021 -  Sufresh Bebida Maracuja.xlsx',
    '24.04.2021 -  Sufresh Bebida Uva.xlsx',
    '27.04.2021 - Sufresh Bebida Morango.xlsx',
    '28.04.2021 - FG Cha Amarelo C Physalis Bxa Cal.xlsx',
    '28.04.2021 - FG Cha Branco Baixa Caloria.xlsx',
    '28.04.2021 - FG Cha Branco C Pitaya Bxa Cal.xlsx',
    '28.04.2021 - FG Cha Branco Com Lichia Bxa Cal.xlsx',
    '28.04.2021 - FG Cha Verde Lar Geng Bxa Cal.xlsx',
    '27.04.2021 - FG Cha Verde Com Limao Bxa Cal.xlsx',
    '27.04.2021 - FG Cha Verde com Cranberry Baixa.xlsx',
    '27.04.2021 - FG Cha Vermelho C. Amora.xlsx',
]

col_map_in = {
    'Tipo : ': 'ptype',
    'Componente/Material': 'citem',
    'Descrição': 'item',
    'Receita': 'rec',
    'Unidade': 'unit',
    'Principal/Semi-Acabado': 'cparent',
    '% Perda': 'loss',
    'Quantidade': 'quant_org',
    'Coeficiente': 'coef',
    'Quantidade Total': 'qtot',
    'À Requisitar': 'quant',
    'Arredondado': 'round',
}

col_map_out = {
     'cprod': 'Código',
     'prod': 'Produto',
     'ind': 'Industrializador',
     'type': 'Tipo de Insumo',
     'citem': 'Cód. Insumo',
     'item': 'Desc. Insumo',
     'unit': 'Unidade',
     'quant': 'Quantidade',
     'loss': 'Perda',
}

ptype = {
    'mp': '2-MATERIA PRIMA',
    'semi': '1-SEMI ACABADO ',
}
params_db = {
    'CoPacker': '/Users/maxi/Documents/WOW/CUSTOS/TST/DOWNLOAD/prod_ind.xlsx',
    'MaterialTypes': '/Users/maxi/Documents/WOW/CUSTOS/TST/DOWNLOAD/mat_types.xlsx',
}

def read_bom_newage(wbooks, col_map,):
    ind = pd.read_excel(params_db['CoPacker'])
    mat = pd.read_excel(params_db['MaterialTypes'])
    # make sure that prodcodes are strings
    cur_prods= set([ str(cprod) for cprod in list(ind['cprod']) ])
    new_cols = [ val for _, val in col_map.items() ]
    col_nums = [i for i in range(len(col_map))]

    dfs = dict()
    for wbook_abs in wbooks:
        wbook = os.path.basename(wbook_abs)
        dfs[wbook] = pd.read_excel(wbook_abs, sheet_name=None, skiprows=6,
                                   header=None, usecols=col_nums, names=new_cols)
        dfs_curr = dfs[wbook]

        # Remove all sheets whose name is not a valid current product code
        sheets = { s for s in dfs_curr }
        for s in sheets - cur_prods:
            print(f'Excluding sheet {s} from {wbook}')
            dfs_curr.pop(s)

        # add a cprod column
        for cprod in dfs_curr:
            df = dfs_curr[cprod]
            df['cprod'] =int(cprod)

    #build the complete BOM dataframe
    df_to_concat = [ dfs[wbook][sheet] for wbook in dfs for sheet in dfs[wbook] ]
    if df_to_concat == []:
        return None, 'no-data'
    df_bom = pd.concat(df_to_concat)

    # Drop any lines with empty product codes
    try:
        df_bom.drop(df_bom.loc[df['citem'].isna(),:].index, inplace=True)
    except pd.core.indexing.IndexingError:
        pass

    # Drop all entries of intermediary products
    try:
        df.drop(index=df.loc[df['ptype'] == ptype['semi'],:].index, inplace=True)
    except pd.core.indexing.IndexingError:
        pass

    # Drop all columns we are not interested in
    cols_to_drop = list(set(df.columns) - set([*col_map_out]))
    df.drop(columns=cols_to_drop, inplace=True)

    # remove leading or trailing blanks in all string columns
    strip_chars(df_bom,' \t')

    # put in prod and ind columns with correct values
    df_bom = df_bom.merge(ind[['cprod', 'prod', 'ind']], how='left', on='cprod')

    # put in item and type columns with correct values
    df_bom = df_bom.merge(mat[['citem', 'type']], how='left', on='citem')

    # TODO: Check how to update the material types if receitas change
    # Drop all lines which do no have a material type ->they are not being purchased
    try:
        df_bom.drop(df_bom.loc[df_bom['type'].isna(),:].index, inplace=True)
    except pd.core.indexing.IndexingError:
        pass

    # Adjust quantities to unit
    # for each product use the maximum value of quant as number of units per caixa
    # calculate #units per box for each product
    units_box = df_bom[['cprod', 'quant']]\
                .groupby('cprod', as_index=False)\
                .apply(max)\
                .rename(columns={'quant':'un_cx'})
    df_bom = df_bom.merge(units_box, how='left', on='cprod')

    # Adjust the volume for all envase services by the number of units per box
    # envase is by CX in NewAge ad by unit in Claudia's excel
    # Adjust envase values
    ix = df_bom.loc[(df_bom['type'] == 'ENV') & (df_bom['unit'] == 'CX'),:].index
    if not ix.empty:
        df_bom.loc[ix, 'quant'] = df_bom.loc[ix, 'quant'] * df_bom.loc[ix, 'un_cx']
    # divide all values by number of units per box
    df_bom['quant'] = df_bom['quant'] / df_bom['un_cx']

    df_bom = df_bom[[*col_map_out]]

    return df_bom, 'ok'


###################### Functions to read Excel files into Pandas #############
def read_excel(file_name, *args, **kwargs):
    """Doc String."""
    df = None
    ret = ('ok', None)
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


def strip_chars(df,  columns=frozenset(), chars=None,):
    for c in set(df.columns) - set(columns):
        if df[c].dtype == object:
            try:
                df[c] = df[c].str.strip(chars)
            except AttributeError:
                pass
    return df


if __name__ == '__main__':
    base_dir = '/Users/maxi/Documents/WOW/CUSTOS/TST/DOWNLOAD'
    df, ret = read_bom_newage([ os.path.join(base_dir, wb) for wb in wbooks ], col_map_in)
    df_writer = lambda x='estrutura_newage.xlsx': df.rename(columns=col_map_out).to_excel(x)
