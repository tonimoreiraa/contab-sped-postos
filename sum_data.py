def sum_input_data(input_data):
    type = 'tanque'
    data = []
    for rows in input_data:
        # tanque, bico
        for id in rows.keys():
            key = 'aferição' if type == 'bico' else 'recebimento'
            value = 0
            for x in rows[id]:
                value = value + float(x[key].replace('.', '').replace(',', '.'))
            data.append({'type': type, type: int(id), 'value': value, 'key': key})
        type = 'bico'

    return data
