import PyPDF2
import re
from format_value import format_value

def extract_data(file_path):
    pdf_reader = PyPDF2.PdfReader(file_path)
    extracted_data = []

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        
        # Extrai dados da tabela "POSIÇÃO DOS TANQUES"
        if "POSIÇÃO DOS TANQUES" in text:
            matches = re.findall(r'\| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?)\n', text)
            for match in matches:
                if all(match):  # Garante que todas as informações foram extraídas
                    extracted_data.append({
                        'Info': match[0],
                        'Abertura': format_value(match[1]),
                        'Fechamento': format_value(match[2]),
                        'Campo1': format_value(match[4]),
                        'Campo2': format_value(match[5]),

                    })
    return extracted_data

def capture_tank_number(input_string):
    # Divide a string em partes por espaços
    parts = input_string.split()
    # Captura o número do tanque (segundo elemento da lista)
    tank_number = parts[1]
    # Remove zeros à esquerda
    cleaned_number = tank_number.lstrip('0')
    # Se cleaned_number estiver vazio após remover zeros à esquerda, significa que era "00000"
    return cleaned_number if cleaned_number else '0'

def get_data(cnpj, file_path):
    extracted_data = extract_data(file_path)

    bico = []
    tanque = []
    bico_tanque_data = []
    for item in extracted_data:
        if 'Produto' in item['Info']:
            break
        else:
            try:
                bico_id = ''.join(filter(str.isdigit, item['Info']))
                bico_tanque_data.append({
                    'type': 'bico',
                    'bico': int(bico_id),
                    'abertura': item['Abertura'],
                    'fechamento': item['Fechamento'],
                    'afericao': item['Campo1']
                })
            except:
                pass
                
    for item in extracted_data:
        if 'TANQUE' in item['Info']:
            tanque_id = capture_tank_number(item['Info'])
            bico_tanque_data.append({
                'type': 'tanque',
                'tanque': int(tanque_id),
                'abertura': item['Abertura'], 
                'fechamento': item['Campo2'],
                'recebimento': None
            })
    path_xlsx = f"output/{cnpj}.xlsx"
    path_dac = f"input/dac/{cnpj}.txt"
    return bico_tanque_data, cnpj, path_dac, path_xlsx