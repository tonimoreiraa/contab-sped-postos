import PyPDF2
import re
from format_value import format_value

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_data(text):
    data_bico = []
    data_tanque = []

    # Padrões regex para cada campo
    produto_pattern = r"-\s*(.+?)\s*\d\)\s*D\.\s*Inicial"
    tanque_pattern = r"TQ\s+TQ\s+(\d+)\s+(\d{1,3}(?:\.\d{3})*(?:,\d{1,2})?)"
    estoque_abertura_pattern = r"3\.1\) Estoque de Abertura\s+([\d.,]+)"
    volume_recebido_pattern = r"4\.3\) Total Recebido\s+([\d.,]+)"
    estoque_fechamento_pattern = r"7\) Estoque de Fechamento\s*\(.*?\)\s*(\d+[\.,]\d*)"
    vendas_bico_pattern = r"(\d+)\s+(\d+)\s+([\d.]+,[\d]+)\s+([\d.]+,[\d]+)\s+([\d.]+,[\d]+)\s+([\d.]+,[\d]+)"
    
    # Encontrando todas as ocorrências de cada campo
    produtos = re.findall(produto_pattern, text)
    tanques = re.findall(tanque_pattern, text)
    estoques_abertura = re.findall(estoque_abertura_pattern, text)
    volumes_recebidos = re.findall(volume_recebido_pattern, text)
    estoque_fechamento = re.findall(estoque_fechamento_pattern, text)
    vendas_bico = re.findall(vendas_bico_pattern, text)


    # Agrupando os dados de Tanque
    for i in range(len(produtos)):
        tanque_info = {
            "type": "tanque",
            "tanque": tanques[i][0],
            #"produto": produtos[i],
            "abertura": format_value(estoques_abertura[i]) if i < len(estoques_abertura) else 0,
            "fechamento": format_value(estoque_fechamento[i]) if i < len(estoque_fechamento) else 0,
            "recebimento": format_value(volumes_recebidos[i]) if i < len(volumes_recebidos) else 0,
            "venda": 0
        }
        #print("Tanque info:", tanque_info)
        data_tanque.append(tanque_info)

    # Agrupando os dados de Bico
    for match in vendas_bico:
        bico_info = {
            #"Tanque": match[0],
            "type": "bico",
            "bico": match[1],
            #"produto": None, # para adicionar
            "abertura": format_value(match[3]),
            "fechamento": format_value(match[2]),
            #"Sem_intervencao": None,
            #"Com_intervencao": None,
            "afericao": format_value(match[4]),
            "venda": format_value(match[5])
        }
        #print("Bico info:", bico_info)
        data_bico.append(bico_info)

    return data_tanque, data_bico

def get_data(cnpj, file_path):
    pdf_text = extract_text_from_pdf(file_path)
    
    tanque_data, bico_data = extract_data(pdf_text)
    bico_tanque_data = []
    for bico in bico_data:
        bico_tanque_data.append(bico)
    for tanque in tanque_data:
        bico_tanque_data.append(tanque)

    path_xlsx = f"output/{cnpj}.xlsx"
    path_dac = f"input/dac/{cnpj}.txt"
    return bico_tanque_data, cnpj, path_dac, path_xlsx