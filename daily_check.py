def is_closure_equal_to_opening(first_row, next_row):
    if not next_row:
        return True
    if first_row['fechamento'] != next_row['abertura']:
        return float("{:.3f}".format(abs(first_row['fechamento'] - next_row['abertura'])))
    
    return first_row['fechamento'] == next_row['abertura']

def daily_check(data):
    output = []
    type = 'tanque'
    for rows in data:
        for id in rows.keys():
            rows_length = len(rows[id])
            for i in range(0, rows_length):
                current_row = rows[id][i]
                is_error = is_closure_equal_to_opening(rows[id][i], rows[id][i+1] if i < rows_length - 1 else None)
                o = {
                    "Tipo": type,
                    type: current_row[type],
                    "Ordem": i,
                    "Abertura": current_row['abertura'],
                    "Fechamento": current_row['fechamento'],
                    "Conferência": is_error
                }
                output.append(o)
            
        type = 'bico'

    return output