def read_input(input_path):
    try:
        input_file = open(input_path, 'r', encoding='utf-8', errors='ignore')
        content = input_file.read()
        tanque_data = {}
        bico_data = {}
        for row in content.split('\n'):
            row_data = row.split('|')
            if len(row_data) > 1:
                if row_data[1] == '1310':
                    tanque_id = int(row_data[2])
                    if not tanque_id in tanque_data:
                        tanque_data[tanque_id] = []
                    keys = ['tanque', 'abertura', 'recebimento', 'estoque disponivel', 'venda', 'estoque escritural', 'ganho', 'perda', 'fechamento']
                    dict = { key: float(value.replace('.', '').replace(',', '.')) for key, value in zip(keys, row_data[2:]) }
                    tanque_data[tanque_id].append(dict)
                elif row_data[1] == '1320':
                    bico_id = int(row_data[2])
                    if not bico_id in bico_data:
                        bico_data[bico_id] = []
                    keys = ['bico', 'fechamento', 'abertura', 'aferição', 'venda']
                    row_data = [row_data[2]] + row_data[8:]
                    dict = { key: float(value.replace('.', '').replace(',', '.')) for key, value in zip(keys, row_data) }
                    bico_data[bico_id].append(dict)

        return [tanque_data, bico_data]
    except Exception as e:
        print(e)
        return False