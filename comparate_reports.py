def comparate(input_data, report_data):

    output = []
    # Tanque
    receb_rep, venda_rep, receb_sped, venda_sped = [0,0,0,0]
    tanque_data = input_data[0]

    for id in tanque_data.keys():
        rows_length = len(tanque_data[id])
        abertura = tanque_data[id][0]['abertura']
        fechamento = tanque_data[id][rows_length - 1]['fechamento']
        recebimento = sum(item['recebimento'] for item in tanque_data[id])
        venda = sum(item['venda'] for item in tanque_data[id])
        
        report_item = next((item for item in report_data[0] if item.get('type') == 'tanque' and int(item.get('tanque')) == int(id)), None)
        if report_item != None:
            receb_rep += report_item['recebimento']
            receb_sped += recebimento
            venda_rep += report_item['venda']
            venda_sped += venda

            output.append({
                'type': 'tanque',
                'tanque': int(id),
                'abertura sped': abertura,
                'abertura relatório': report_item['abertura'],
                'conferência abertura': "VERDADEIRO" if report_item['abertura'] == abertura else float("{:.3f}".format(abs(report_item['abertura'] - abertura))),
                'fechamento sped': fechamento,
                'fechamento relatório': report_item['fechamento'],
                'conferência fechamento': "VERDADEIRO" if report_item['fechamento'] == fechamento else float("{:.3f}".format(abs(report_item['fechamento'] - fechamento))),
                'recebimento sped': recebimento,
                'recebimento relatório': report_item['recebimento'],
                'conferência recebimento': "VERDADEIRO" if report_item['recebimento'] == recebimento else float("{:.3f}".format(abs(report_item['recebimento'] - recebimento))),
                'venda sped': venda,
                'venda relatório': report_item['venda'],
                'conferência venda': "VERDADEIRO" if report_item['venda'] == venda else float("{:.3f}".format(abs(report_item['venda'] - venda)))
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
                'conferência recebimento': 'Não encontrado',
                'venda sped':venda,
                'venda relatório': 'Não encontrado',
                'conferência venda': 'Não encontrado'
            })

    output.append({
                'type': 'tanque',
                'tanque': 'TOTAL',
                'abertura sped': '',
                'abertura relatório': '',
                'conferência abertura': '',
                'fechamento sped': '',
                'fechamento relatório': '',
                'conferência fechamento': '',
                'recebimento sped': receb_sped,
                'recibimento relatório': receb_rep,
                'conferência recebimento': "VERDADEIRO" if receb_rep == receb_sped else float("{:.3f}".format(abs(receb_rep - receb_sped))),
                'venda sped':venda_sped,
                'venda relatório': venda_rep,
                'conferência venda': "VERDADEIRO" if venda_rep == venda_sped else float("{:.3f}".format(abs(venda_rep - venda_sped)))
            })

    # Bico
    receb_rep, venda_rep, receb_sped, venda_sped = [0,0,0,0]
    bico_data = input_data[1]
    for id in bico_data.keys():
        rows_length = len(bico_data[id])
        abertura = bico_data[id][0]['abertura']
        fechamento = bico_data[id][rows_length - 1]['fechamento']
        afericao = sum(item['aferição'] for item in bico_data[id])
        venda = sum(item['venda'] for item in bico_data[id])

        report_item = next((item for item in report_data[0] if item.get('type') == 'bico' and int(item.get('bico')) == int(id)), None)
        

        if report_item != None:
            receb_rep += report_item['afericao']
            receb_sped += afericao
            venda_rep += report_item['venda']
            venda_sped += venda

            output.append({
                'type': 'bico',
                'bico': int(id),
                'abertura sped': abertura,
                'abertura relatório': report_item['abertura'],
                'conferência abertura': "VERDADEIRO" if report_item['abertura'] == abertura else float("{:.3f}".format(abs(report_item['abertura'] - abertura))),
                'fechamento sped': fechamento,
                'fechamento relatório': report_item['fechamento'],
                'conferência fechamento': "VERDADEIRO" if report_item['fechamento'] == fechamento else float("{:.3f}".format(abs(report_item['fechamento'] - fechamento))),
                'aferição sped': afericao,
                'aferição relatório': report_item['afericao'],
                'conferência aferição': "VERDADEIRO" if report_item['afericao'] == afericao else float("{:.3f}".format(abs(report_item['afericao'] - afericao))),
                'venda sped': venda,
                'venda relatório': report_item['venda'],
                'conferência venda': "VERDADEIRO" if report_item['venda'] == venda else float("{:.3f}".format(abs(report_item['venda'] - venda)))
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
                'conferência aferição': 'Não encontrado',
                'venda sped':venda,
                'venda relatório': 'Não encontrado',
                'conferência venda': 'Não encontrado'
            })
    output.append({
                'type': 'bico',
                'tanque': 'TOTAL',
                'abertura sped': '',
                'abertura relatório': '',
                'conferência abertura': '',
                'fechamento sped': '',
                'fechamento relatório': '',
                'conferência fechamento': '',
                'recebimento sped': receb_sped,
                'recibimento relatório': receb_rep,
                'conferência recebimento': "VERDADEIRO" if receb_rep == receb_sped else float("{:.3f}".format(abs(receb_rep - receb_sped))),
                'venda sped':venda_sped,
                'venda relatório': venda_rep,
                'conferência venda': "VERDADEIRO" if venda_rep == venda_sped else float("{:.3f}".format(abs(venda_rep - venda_sped)))
            })
    return output