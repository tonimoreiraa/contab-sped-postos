#input_path = ''

def read_input(input_path):
    try:
        input_file = open(input_path, 'r', encoding='utf-8')
        content = input_file.read()
    except UnicodeDecodeError:
        # Tente uma codificação alternativa se a padrão falhar
        input_file = open(input_path, 'r', encoding='ISO-8859-1')
        content = input_file.read()
        
    tanque_data = {}
    bico_data = {}
    for row in content.split('\n'):
        row_data = row.split('|')
        if len(row_data) > 1:
            if row_data[1] == '1310':
                tanque_id = row_data[2]
                if not tanque_id in tanque_data:
                    tanque_data[tanque_id] = []
                keys = ['tanque', 'abertura', 'recebimento', 'estoque disponivel', 'venda', 'estoque escritural', 'ganho', 'perda', 'fechamento']
                dict = { key: value for key, value in zip(keys, row_data[2:]) }
                tanque_data[tanque_id].append(dict)
            elif row_data[1] == '1320':
                bico_id = row_data[2]
                if not bico_id in bico_data:
                    bico_data[bico_id] = []
                keys = ['bico', 'fechamento', 'abertura', 'aferição', 'venda']
                row_data = [row_data[2]] + row_data[8:]
                dict = { key: value for key, value in zip(keys, row_data) }
                bico_data[bico_id].append(dict)

    return [tanque_data, bico_data]

def is_closure_equal_to_opening(first_row, next_row):
    if not next_row:
        return True
    
    return first_row['fechamento'] == next_row['abertura']

"""data = read_input(input_path)
tanque_data, bico_data = data
type = 'tanque'

for rows in data:
    for id in rows.keys():
        errors = 0
        rows_length = len(rows[id])
        for i in range(0, rows_length):
            if i < rows_length - 1:
                if not is_closure_equal_to_opening(rows[id][i], rows[id][i+1]):
                    row = rows[id][i]
                    next_row = rows[id][i+1]
                    errors = errors + 1
                    print('%s %s com fechamento %s é diferente da próxima abertura (%s: %s)' % (type, row[type], row['fechamento'], next_row[type], next_row['abertura'] ))

        print('Conferência %s %s com %s/%s erros' % (type, id, errors, rows_length))
        
    type = 'bico'
"""