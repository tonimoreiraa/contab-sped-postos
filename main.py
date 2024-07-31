import os
from input import read_input
from daily_check import daily_check
from identify_models import identify_report_model
from models import models
from sum_data import sum_input_data

input_path = 'input/dac'
report_path = 'input/relatorio'

files_and_dirs = os.listdir(input_path)
cnpjs = [f.replace('.txt', '') for f in files_and_dirs if os.path.isfile(os.path.join(input_path, f))]


for cnpj in cnpjs:
    input_data = read_input(os.path.join(input_path, cnpj + '.txt'))
    daily_output = daily_check(input_data)
    # TODO: save daily_output to output xlsx

    report_file_path = os.path.join(report_path, cnpj)
    if os.path.exists(report_file_path + '.pdf'):
        report_file_path = report_file_path + '.pdf'
    else:
        report_file_path = report_file_path + '.xlsx'

    report_model = identify_report_model(report_file_path)

    report_data = None
    if report_model != 'Modelo desconhecido':
        report_data = models[report_model](cnpj, report_file_path)
    else:
        print(f'Relatório do CNPJ {cnpj} não foi reconhecido como um modelo cadastrado')

    # TODO: Verificar se report_data bate com input_data
    
    sum_data = sum_input_data(input_data)
    
    # TODO: Verificar se sum_data base com report_data