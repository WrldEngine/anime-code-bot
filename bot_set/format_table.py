def print_pretty_table(data, cell_sep=' | ', header_separator=True):
    n = ''
    rows = len(data)
    cols = len(data[0])

    col_width = []
    for col in range(cols):
        columns = [data[row][col] for row in range(rows)]
        col_width.append(len(max(columns, key=len)))

    for i, row in enumerate(range(rows)):
        result = []
        for col in range(cols):
            item = data[row][col].rjust(col_width[col])
            result.append(item)

        n += cell_sep.join(result) + '\n'
    return n