import pandas as pd

def tableize(df, size: int = 20):
    """
    Pretty-print a DataFrame as a table, with an optional row limit.

    Args:
        df (pd.DataFrame): The DataFrame to print.
        size (int): Maximum number of rows to display (default: 20).
    """
    if not isinstance(df, pd.DataFrame):
        return
    df_columns = df.columns.tolist()
    max_len_in_lst = lambda lst: len(max([str(x) for x in lst], key=len))
    align_center = lambda st, sz: "{0}{1}{0}".format(" " * (1 + (sz - len(st)) // 2), st)[:sz] if len(st) < sz else st
    align_right = lambda st, sz: "{0}{1} ".format(" " * (sz - len(st) - 1), st) if len(st) < sz else st
    max_col_len = max_len_in_lst(df_columns)
    max_val_len_for_col = {col: max_len_in_lst(df.iloc[:, idx].astype(str)) for idx, col in enumerate(df_columns)}
    col_sizes = {col: 2 + max(max_val_len_for_col.get(col, 0), max_col_len) for col in df_columns}
    build_hline = lambda row: '+'.join(['-' * col_sizes[col] for col in row]).join(['+', '+'])
    build_data = lambda row, align: "|".join([align(str(val), col_sizes[df_columns[idx]]) for idx, val in enumerate(row)]).join(['|', '|'])
    hline = build_hline(df_columns)
    out = [hline, build_data(df_columns, align_center), hline]
    for i, (_, row) in enumerate(df.iterrows()):
        if i >= size:
            out.append(f"|{'...'.center(sum(col_sizes.values()) + len(col_sizes) - 1)}|")
            break
        out.append(build_data(row.tolist(), align_right))
    out.append(hline)
    return "\n".join(out)