import PyPDF2
import re

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
                        'Abertura': match[1],
                        'Fechamento': match[2],
                        'Campo1': match[4],
                        'Campo2': match[5],

                    })
    return extracted_data

def get_data(file_name):
    p, x = ".pdf", ".xlsx"
    cnpj = ""
    if p in file_name:
        cnpj = str(file_name).replace(p,"")
    else:
        cnpj = str(file_name).replace(x,"")

    file_path = f"input/relatorio/{file_name}"

    extracted_data = extract_data(file_path)

    bico_words = ['GC','DC','DS','GA','EC']
    tanque_words = ['GAS', 'ETAN', 'DIES']

    bico = []
    tanque = []
    for item in extracted_data:
        if 'Produto' in item['Info']:
            break
        else:
            for word in bico_words:
                if word in item['Info']:
                    bico_id = str(item['Info']).replace(word, "")
                    bico_id = int(bico_id)
                    bico.append({
                        'Bico': bico_id,
                        'Produto': word, 
                        'Abertura': item['Abertura'],
                        'Fechamento': item['Fechamento'],
                        'Sem_intervencao': None,
                        'Com_intervencao': None,
                        'Afericao': item['Campo1']
                    })
                
    for item in extracted_data:
        if 'TANQUE' in item['Info']:
            for word in tanque_words:
                if word in item['Info']:
                    tanque_id = str(item['Info']).replace("TANQUE ", "")
                    tanque_id = tanque_id.replace("///", "")
                    tanque_id = tanque_id.replace(word, "")
                    tanque_id = int(tanque_id)
                    tanque.append({
                        'Tanque': tanque_id,
                        'Produto': word, 
                        'Abertura': item['Abertura'], 
                        'Fechamento': item['Campo2'],
                        'Afericao': item['Campo1']
                    })
    path_xlsx = f"output/{cnpj}.xlsx"
    path_dac = f"input/dac/{cnpj}.txt"
    return bico, tanque, cnpj, path_dac, path_xlsx