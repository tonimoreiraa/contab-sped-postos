import os
from identify_models import identify_report_model
from sped_vs_rep import sped_vs_rep
import model_a
import model_b
import model_c
import model_d
import model_e
import model_f
import model_g
import model_h
import model_i

dir = 'input/relatorio/'
files = os.listdir(dir)

files = [f for f in files if os.path.isfile(os.path.join(dir, f))]

model_dict = {
    'A': model_a.get_data,
    'B': model_b.get_data,
    'C': model_c.get_data,
    'D': model_d.get_data,
    'E': model_e.get_data,
    'F': model_f.get_data,
    'G': model_g.get_data,
    'H': model_h.get_data,
    'I': model_i.get_data
}

for file in files:
    file_path = dir+file
    model = identify_report_model(file_path)
    if model != 'Modelo desconhecido':
        cnpj = ''.join(filter(str.isdigit, file))
        bico_tanque_data, company, path_dac, xlsx_path = model_dict[model](cnpj, file_path)
        bico_data, tanque_data = [], []
        for data in bico_tanque_data:
            if data['type'] == 'bico':
                bico_data.append(data)
            else:
                tanque_data.append(data)
        sped_vs_rep(bico_data, tanque_data, company, path_dac, xlsx_path)
    else:
        print('Arquivo com modelo desconhecido: %s' % (file_path))

