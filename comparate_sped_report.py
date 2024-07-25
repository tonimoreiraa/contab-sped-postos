import os
from identify_file_model import identify_file_model
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
    model = identify_file_model(file_path)
    if model != 'Modelo desconhecido':
        bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path = model_dict[model](file)
        sped_vs_rep(bico_data_from_rep, tanque_data_from_rep, company, path_dac, xlsx_path)
    else:
        print('Arquivo com modelo desconhecido: %s' % (file_path))

