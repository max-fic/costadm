#! /usr/bin/env python
import pandas as pd

def gen_weighted_func(col, **kwargs):
    """
    generate a weighted aggregation function like
    a weighted sum or averag to be used with df.apply
    or df.group.agg

    When called by df.apply or df.group the function multiplies its
    parameters (grp) with the values the weights in column col.
    the function func will be applied to the multiplied values
    If abs=False is speciffied the result will be divided by the 
    the sum of the weights. Finally func will be applied the resulting 
    values.

    When used  with df.apply or dfgroup.agg the original dataframe must
    be passed (in this case wieghted_func is passed only a series)
    When used with dfgroup.apply the data frame can be omitted as 
    weighted_func receives a dataframe which includes the weights column
    """
    def weighted_func(grp):
        nonlocal col, df, func, is_abs

        df_loc = grp if df is None else df 
        v_col = df_loc.loc[grp.index,col]

        # either calc func(a*b) (absolute values)
        # or func((a*b)/sum(a)) relative values
        denom = 1 if is_abs else func(v_col)
        num = grp.multiply(v_col, axis=0)
        return func(num / denom)

    df = kwargs.get('df', None)
    func = kwargs.get('func', sum)
    is_abs = kwargs.get('abs', True)

    return weighted_func


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
