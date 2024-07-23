import PyPDF2
import re

cnpj = "25023880000142"
empresa = "AUTO POSTO SMART LTDA  EPP"

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

    # Verificando se todos os campos foram encontrados
    #print(f"Produtos encontrados: {produtos}")
    #print(f"Tanques encontrados: {tanques}")
    #print(f"Estoques de Abertura encontrados: {estoques_abertura}")
    #print(f"Volumes Recebidos encontrados: {volumes_recebidos}")
    #print(f"Estoques de Fechamento encontrados: {estoque_fechamento}")
    #print(f"Vendas Bico encontradas: {vendas_bico}")

    # Agrupando os dados de Tanque
    for i in range(len(produtos)):
        tanque_info = {
            "Tanque": tanques[i][0],
            "Produto": produtos[i],
            "Abertura": estoques_abertura[i] if i < len(estoques_abertura) else "N/A",
            "Fechamento": estoque_fechamento[i] if i < len(estoque_fechamento) else "N/A",
            "Recebimento": volumes_recebidos[i] if i < len(volumes_recebidos) else "N/A"
        }
        #print("Tanque info:", tanque_info)
        data_tanque.append(tanque_info)

    # Agrupando os dados de Bico
    for match in vendas_bico:
        bico_info = {
            #"Tanque": match[0],
            "Bico": match[1],
            "Produto": None, # para adicionar
            "Abertura": match[3],
            "Fechamento": match[2],
            "Sem_intervencao": None,
            "Com_intervencao": None,
            "Afericao": match[4],
            #"VendaBico": match[5]
        }
        #print("Bico info:", bico_info)
        data_bico.append(bico_info)

    return data_tanque, data_bico

def get_data():
    try:
        file_path = f"input/relatorio/{cnpj}.pdf"
        pdf_text = extract_text_from_pdf(file_path)
    except:
        file_path = f"input/relatorio/{cnpj}.xlsx"
        pdf_text = extract_text_from_pdf(file_path)
    
    data_tanque, data_bico = extract_data(pdf_text)

    path_xlsx = f"output/{cnpj}.xlsx"
    path_dac = f"input/dac/{cnpj}.txt"
    return data_bico, data_tanque, empresa, path_dac, path_xlsx
