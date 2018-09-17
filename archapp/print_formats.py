"""
print_formats.py defines utilities for formatting text data
"""

import os
import math

def print_xarray(xarr, field, fill=True):
    """
    Print the field of every key in input xarray

    Parameters
    ----------
    xarr : xarray.Dataset
        contains some number of xarray datasets
    field : string
        field to print
    """
    try:
        df = xarr.to_dataframe()
    except IndexError:
        print("No valid PVs to print!")
        return
    df = df.T[field].T
    if fill:
        # fill nan w/ previous value
        df = df.fillna(method="pad")
        # remove all prepended nan
        while any(df.iloc[0].isnull()):
            df = df.iloc[1:]
        print(df.to_string())
    else:
        shortest = None
        for pv in list(df.keys()):
            nchar = len(pv)
            if shortest is None or nchar < shortest:
                shortest = nchar
        print(df.fillna("-"*shortest).to_string())


def list_print(data, width=0, do_print=True):
    """
    Prints list data in columns as you'd expect from a terminal.

    Parameters
    ----------
    data : list

    width : int
        if >  0: absolute display with
        if == 0: terminal width
        if <  0: terminal width + int

    do_print : bool
        If False, return text

    Returns
    -------
    rows : list of string or bool
    """
    if len(data) == 0:
        return False
    text_data = [str(i) for i in data]
    col_width = max([len(i) for i in text_data]) + 2
    if width <= 0:
        _, term_width = os.popen('stty size', 'r').read().split()
        term_width = int(term_width)
        if width < 0:
            term_width += width
    else:
        term_width = width
    n_cols = term_width/col_width
    n_text = len(text_data)
    n_full_col = int(math.ceil(float(n_text) / n_cols))
    text_rows = []
    for i in range(n_full_col):
        text_rows.append([])
    row = 0
    for text in text_data:
        text_rows[row].append(text)
        if row < n_full_col - 1:
            row += 1
        else:
            row = 0
    line_elem = "{0:{1}}"
    if not do_print:
        rows = []
    for row in text_rows:
        line = ""
        for text in row:
            line += line_elem.format(text, col_width)
        if do_print:
            print(line)
        else:
            rows.append(line)
    if do_print:
        return True
    else:
        return rows
