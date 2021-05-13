# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name
# pylint: disable=fixme

import os
import pandas as pd
from pandas_helper import read_sheet

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

colmap_newage_in = {
    'Tipo : ': 'ptype',
    'Componente/Material': 'citem',
    'Descrição': 'item',
    'Receita': 'rec',
    'Unidade': 'unit',
    'Principal/Semi-Acabado': 'cparent',
    # '% Perda': 'loss',
    'Quantidade': 'quant_org',
    'Coeficiente': 'coef',
    'Quantidade Total': 'qtot',
    'À Requisitar': 'quant',
    'Arredondado': 'round',
}


colmap_bom_in = {
    'Código': ('cprod', 'int'),
    'Produto': ('prod', 'str'),
    'Industrializador': ('ind', 'str'),
    'Tipo de Insumo': ('type', 'str'),
    'Cód. Insumo': ('citem', 'str'),
    'Desc. Insumo': ('item', 'str'),
    'Unidade': ('unit', 'str'),
    'Quantidade': ('quant', 'number'),
    # 'Perda': ('loss', 'number'),
    # 'Custo': ('cost', 'int'),
}


colmap_quotes_in = {
    'Código': ('citem', 'str'),
    'Descrição': ('item', 'str'),
    'ICMS': ('icms%', 'float'),
    'IPI': ('ipi%',  'float'),
    'Pis/Cofins': ('pis%', 'float'),
    'Preço Convertido R$ c/IPI': ('costtax_item', 'float'),
    'Preço NET s/impostos c/frete': ('cost_item', 'float')
}

colmap_prods_in = {
    'CÓD.PROD.': ('cprod', 'int'),
    'NOME_PRODUTO': ('prod', 'str'),
    'Industrializador': ('ind', 'str'),
    'Porcentagem': ('percent', 'number')
}

colmap_recipe_in = {
    'Matéria-prima': ('item', 'str'),
    'Código New Age': ('citem', 'str'),
    'UND': ('unit', 'str'),
    'Quant': ('quant', 'float'),
    'Perda': ('loss', 'float')
}

colmap_out = {
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

def _read_bom_newage(wbooks, col_map, db):
    ind = db.read('copacker')
    mat = db.read('tipo_material')
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
        return None, ('no-data', 'No data to process')
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
    cols_to_drop = list(set(df.columns) - set([*colmap_out]))
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

    df_bom = df_bom[[*colmap_out]]

    return df_bom, ('ok', None)

### Define the external interface
read_bom_newage_db = lambda file, db: _read_bom_newage(file, colmap_newage_in, db)

def read_prod_volumes(file_name):
    return read_sheet(file_name, 0, colmap_prods_in)


def read_quotes(file_name):
    return read_sheet(file_name, 'Preços', colmap_quotes_in)


def read_bom(file_name):
    return read_sheet(file_name, 0, colmap_bom_in)


def make_bom(df, cprod, prod, ind, cost_type, factor):
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


def bom_from_recipes(recipes):
    """Doc String."""
    df_list = []

    for file in recipes:
        print(f'Processing file {file}')
        sh_index, err = read_sheet(file, 'Index', ['cprod', 'prod', 'ind', 'type', 'detail', 'fator'])
        if err[0] != 'ok':
            return None, err

        # Process all items in index
        sh_index = sh_index.dropna(subset=['detail'])
        for cprod, prod, ind, cost_type, detail, factor in zip(sh_index['cprod'], sh_index['prod'], sh_index['ind'],
                                                               sh_index['type'], sh_index['detail'], sh_index['fator']):
            df, err = read_sheet(file, detail, colmap_recipe_in)
            if err[0] != 'ok':
                return None, err
            # print(f'Appending {cprod}, {prod}, ind, {cost_type}')
            df_list.append(make_bom(df, cprod, prod, ind, cost_type, factor))

    return pd.concat(df_list, ignore_index=True), ('ok',None)


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