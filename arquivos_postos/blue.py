import PyPDF2
import re
from save_to_sheet import save_to_sheet

cnpj = "07783800000175"
empresa = "AUTO POSTO BLUE LTDA"

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

def get_data():
    try:
        file_path = f"input/relatorio/{cnpj}.pdf"
    except:
        file_path = f"input/relatorio/{cnpj}.xlsx"

    extracted_data = extract_data(file_path)

    bico_words = ['GC','GA','EH','ODB']
    tanque_words = ['GAS','ETA','GASO','ETAN', 'DIE', 'GASOL']

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
                pattern = r'\b{}\b'.format(re.escape(word))
                if re.search(pattern, item['Info']) != None:
                    tanque_id = str(item['Info']).replace("TANQUE ", "")
                    tanque_id = tanque_id.replace("///", "")
                    new_string = re.sub(pattern, '', tanque_id)
                    new_string = re.sub(r'\s+', ' ', new_string).strip()
                    tanque_id = new_string
                    tanque_id = int(tanque_id)
                    tanque.append({
                        'Tanque': tanque_id,
                        'Produto': word, 
                        'Abertura': item['Abertura'], 
                        'Fechamento': item['Campo2'],
                        'Afericao': item['Campo1']
                    })
    save_to_sheet(bico, tanque, f"output/{cnpj}.xlsx")
    path_dac = f"input/dac/{cnpj}.txt"
    return bico, tanque, empresa, path_dac