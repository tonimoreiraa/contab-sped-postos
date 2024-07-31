import openpyxl

def get_data(cnpj, file_path):
   

    wb = openpyxl.load_workbook(file_path, data_only=True)

    sheet = wb.active
    sheet = wb["Plan1"]

    init = None
    end = None
    for row in sheet.iter_rows():
        if "MOVIMENTAÇÃO DE BOMBAS BICOS E LACRES" in str(row[0].value):
            init = row[0].row
        elif "INFORMAÇÕES MENSAIS DE ESTOQUES DE COMBUSTÍVEIS" in str(row[0].value):
            end = row[0].row
            break  

    list_of_dicts = []

    if init is not None and end is not None and init < end:
        for i in range(init + 10, end):  # init + 8 to skip the header
            row_dict = {cell.column: cell.value for cell in sheet[i] if cell.value is not None}
            list_of_dicts.append(row_dict)  
    else:
        print("Não foi possível encontrar as linhas inicial ou final, ou o intervalo é inválido.")

    bico_data = []
    for list in list_of_dicts:
        if list:
            try:
                bico_data.append({
                    'Bico':list[5],
                    'Produto':list[6],
                    'Abertura':list[8],
                    'Fechamento':list[9],
                    'Sem_intervencao':list[10],
                    'Com_intervencao': None,
                    #'Lacre':list[12],
                    'Afericao':list[13]
                })
            except:
                pass

    list_of_dicts = []

    for i in range(end + 9, sheet.max_row):  # end + 8 to skip the header
        row_dict = {cell.column: cell.value for cell in sheet[i] if cell.value is not None}
        list_of_dicts.append(row_dict)

    tanque_data = []
    for list in list_of_dicts:
        if list:
            try:
                tanque_data.append({
                    'Tanque':list[1],
                    'Produto':list[2],
                    'Abertura':list[4],
                    'Fechamento':list[7],
                    'Recebimento':list[9]
                })
            except:
                pass

    path_dac = f"input/dac/{cnpj}.txt"
    path_xlsx = f"output/{cnpj}.xlsx"
    return bico_data, tanque_data, cnpj, path_dac, path_xlsx