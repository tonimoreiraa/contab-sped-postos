def comparate(input_data, report_data):

    output = []
    # Tanque
    tanque_data = input_data[0]
    for id in tanque_data.keys():
        rows_length = len(tanque_data[id])
        abertura = tanque_data[id][0]['abertura']
        fechamento = tanque_data[id][rows_length - 1]['fechamento']
        recebimento = sum(item['recebimento'] for item in tanque_data[id])

        report_item = next((item for item in report_data[0] if item.get('type') == 'tanque' and int(item.get('tanque')) == int(id)), None)
        if report_item != None:
            output.append({
                'type': 'tanque',
                'tanque': int(id),
                'abertura sped': abertura,
                'abertura relatório': report_item['abertura'],
                'conferência abertura': report_item['abertura'] == abertura,
                'fechamento sped': fechamento,
                'fechamento relatório': report_item['fechamento'],
                'conferência fechamento': report_item['fechamento'] == fechamento,
                'recebimento sped': recebimento,
                'recibimento relatório': report_item['recebimento'],
                'conferência recebimento': report_item['recebimento'] == recebimento
            })
        else:
            output.append({
                'type': 'tanque',
                'tanque': int(id),
                'abertura sped': abertura,
                'abertura relatório': 'Não encontrado',
                'conferência abertura': 'Não encontrado',
                'fechamento sped': fechamento,
                'fechamento relatório': 'Não encontrado',
                'recebimento sped': recebimento,
                'conferência fechamento': 'Não encontrado',
                'recebimento sped': recebimento,
                'recibimento relatório': 'Não encontrado',
                'conferência recebimento': 'Não encontrado'
            })

    # Bico
    bico_data = input_data[1]
    for id in bico_data.keys():
        rows_length = len(bico_data[id])
        abertura = bico_data[id][0]['abertura']
        fechamento = bico_data[id][rows_length - 1]['fechamento']
        afericao = sum(item['aferição'] for item in bico_data[id])

        report_item = next((item for item in report_data[0] if item.get('type') == 'bico' and int(item.get('bico')) == int(id)), None)
        if report_item != None:
            output.append({
                'type': 'bico',
                'bico': int(id),
                'abertura sped': abertura,
                'abertura relatório': report_item['abertura'],
                'conferência abertura': report_item['abertura'] == abertura,
                'fechamento sped': fechamento,
                'fechamento relatório': report_item['fechamento'],
                'conferência fechamento': report_item['fechamento'] == fechamento,
                'aferição sped': afericao,
                'aferição relatório': report_item['afericao'],
                'conferência aferição': report_item['afericao'] == afericao
            })
        else:
            output.append({
                'type': 'bico',
                'bico': int(id),
                'abertura sped': abertura,
                'abertura relatório': 'Não encontrado',
                'conferência abertura': 'Não encontrado',
                'fechamento sped': fechamento,
                'fechamento relatório': 'Não encontrado',
                'aferição sped': afericao,
                'conferência fechamento': 'Não encontrado',
                'aferição sped': afericao,
                'aferição relatório': 'Não encontrado',
                'conferência aferição': 'Não encontrado'
            })

    return output