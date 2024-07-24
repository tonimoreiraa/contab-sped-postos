from sped import check_sped
from save_to_sheet import save_to_sheet

def format_value(value):
    """Converte uma string formatada com vírgula em float"""
    try:
        value = str(value)
        value = value.replace('.', '').strip()
        value = value.replace(',', '.')
        # Converter para float e formatar com duas casas decimais
        value_float = float(value)
        value_formated = "{:.2f}".format(value_float)
        
        return value_formated.replace('.', ',')
    except ValueError:
        return value
        
def sped_vs_rep(bico_data_from_rep, tanque_data_from_rep, empresa, input_path, xlsx_path):
    print(f"*** Processamento de dados da empresa {empresa} Iniciado... ***")
    
    data_from_sped = check_sped(input_path)
    tanque_data_from_sped, bico_data_from_sped = data_from_sped

    first_last_bicos = {}

    for bicos in bico_data_from_sped:
        for rows in bico_data_from_sped[bicos]:
            bico_id = rows['bico']
            if bico_id not in first_last_bicos:
                first_last_bicos[bico_id] = {'first': rows, 'last': rows}
            else:
                first_last_bicos[bico_id]['last'] = rows

    for bicos in bico_data_from_rep:
        errors_ab, errors_fe, errors = [0,0,0]
        for id_bico in first_last_bicos: 
            abertura_sped = format_value(first_last_bicos[id_bico]['first']['abertura'])
            fechamento_sped = format_value(first_last_bicos[id_bico]['last']['fechamento'])

            abertura_rep = format_value(bicos['Abertura'])
            fechamento_rep = format_value(bicos['Fechamento'])
            if int(bicos['Bico']) == int(id_bico):
                if abertura_sped != abertura_rep:
                    errors += 1
                    print(f"Bico [{bicos['Bico']}] apresentou {errors} divergências no valor de |abertura|")
                    print(f"----Valor no relatório: {abertura_rep}| ----Valor no SPED: {abertura_sped}")
                    
                if fechamento_sped != fechamento_rep:
                    errors += 1
                    print(f"Bico [{bicos['Bico']}] apresentou {errors} divergências no valor de |fechamento|")
                    print(f"----Valor no relatório: {fechamento_rep}| ----Valor no SPED: {fechamento_sped}")
                    
        if errors == 0:
            print(f"Tanque [{bicos['Bico']}] foi validado com sucesso! Nenhuma divergência encontrada.")
            bicos['Obs_relatorio'] = "Validado com sucesso! Nenhuma divergência entre o SPED e o relatório foi encontrada!"
        else:
            if errors_ab != 0:
                bicos['Obs_relatorio'] = f"Divergência entre o SPED({abertura_sped}) e o relatório({abertura_rep})!"
            if errors_fe != 0:
                bicos['Obs_relatorio'] = f"Divergência entre o SPED({fechamento_sped}) e o relatório({fechamento_rep})!"

    first_last_tanques = {}

    for tanque in tanque_data_from_sped:
        for rows in tanque_data_from_sped[tanque]:
            tanque_id = rows['tanque']
            if tanque_id not in first_last_tanques:
                first_last_tanques[tanque_id] = {'first': rows, 'last': rows}
            else:
                first_last_tanques[tanque_id]['last'] = rows

    for tanques in tanque_data_from_rep:
        errors_ab, errors_fe, errors = [0,0,0]
        for id_tanque in first_last_tanques: 
            abertura_sped = format_value(first_last_tanques[id_tanque]['first']['abertura'])
            fechamento_sped = format_value(first_last_tanques[id_tanque]['last']['fechamento'])

            abertura_rep = format_value(tanques['Abertura'])
            fechamento_rep = format_value(tanques['Fechamento'])
            if int(tanques['Tanque']) == int(id_tanque):
                if abertura_sped != abertura_rep:
                    errors_ab += 1
                    errors += 1
                    print(f"Tanque [{tanques['Tanque']}] apresentou {errors} divergências no valor de |abertura|:")
                    print(f"----Valor no relatório: {abertura_rep}| ----Valor no SPED: {abertura_sped}")
                if fechamento_sped != fechamento_rep:
                    errors_fe += 1
                    errors += 1
                    print(f"Tanque [{tanques['Tanque']}] apresentou {errors} divergências no valor de |fechamento|:")
                    print(f"----Valor no relatório: {fechamento_rep}| ----Valor no SPED: {fechamento_sped}")
        if errors == 0:
            print(f"Tanque [{tanques['Tanque']}] foi validado com sucesso! Nenhuma divergência encontrada.")
            tanques['Obs_relatorio'] = "Validado com sucesso! Nenhuma divergência entre o SPED e o relatório foi encontrada!"
        else:
            if errors_ab != 0:
                tanques['Obs_relatorio'] = f"Divergência entre o SPED({abertura_sped}) e o relatório({abertura_rep})!"
            if errors_fe != 0:
                tanques['Obs_relatorio'] = f"Divergência entre o SPED({fechamento_sped}) e o relatório({fechamento_rep})!"
                

    save_to_sheet(bico_data_from_rep, tanque_data_from_rep, xlsx_path)
    print(f"*** Processamento de dados da empresa {empresa} finalizado! ***")