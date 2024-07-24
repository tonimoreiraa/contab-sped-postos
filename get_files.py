import os
from identify_file_model import identify_file_model

dir = 'input/relatorio/'
files = os.listdir(dir)

files = [f for f in files if os.path.isfile(os.path.join(dir, f))]

for file in files:
    file_path = dir+file
    model = identify_file_model(file_path)
    print(f"Arquivo {file} é do modelo {model}")