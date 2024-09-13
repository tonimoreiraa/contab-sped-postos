import PyPDF2
import re
from format_value import format_value

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        linhas = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            linhas.extend(page.extract_text().splitlines())  # Adiciona as linhas em uma lista
    return linhas

def extract_bico_data(linhas):
    # Regex para extrair os dados dos bicos
    regex_bicos = re.compile(r"(\d+)\s+([\d.,]+)\s+([\d.,]+)\s+(\d+)\s+([\d.,]+)\s+([\d.,]+)\s+([A-Z0-9\s]+)\s+(\d+)\s+(\d+)\s+([\d.,]+)")

    dados_bicos = {}
    new_text = ""
    for i in range(0, len(linhas)):
        if "MOVIMENTAÇÃO POR BICO COMBUSTÍVEL" in linhas[i]:
            while("MOVIMENTAÇÃO POR TANQUE" not in linhas[i]):
                new_text += linhas[i] + "\n"
                i+=1

    # Encontrar todas as correspondências
    matches = regex_bicos.findall(new_text)

    # Processar as correspondências
    dados_bicos = []
    for match in matches:
        lacre, afericao, com_interv, bomba, encerrante_final, encerrante_inicial, combustivel, tanque, bico, sem_interv = match
        dados_bicos.append({
            "type":"bico",
            #"Lacre": int(lacre),
            "bico": int(bico),
            #"produto": combustivel.strip(),
            "abertura": float(encerrante_inicial.replace(".", "").replace(",", ".")),
            "fechamento": float(encerrante_final.replace(".", "").replace(",", ".")),
            #"Sem_intervenção": float(sem_interv.replace(".", "").replace(",", ".")),
            #"Com_intervenção": float(com_interv.replace(".", "").replace(",", ".")),
            "afericao": float(afericao.replace(".", "").replace(",", ".")),
            "venda": 0,
            #"Bomba": int(bomba),
            #"Tanque": int(tanque),
        })
    return dados_bicos

def extract_tanque_data(linhas):
    new_text = ""
    for i in range(0, len(linhas)):
        if "MOVIMENTAÇÃO POR TANQUE" in linhas[i]:
            while("MOVIMENTAÇÃO POR CFOP" not in linhas[i]):
                new_text += linhas[i] + "\n"
                i += 1

    regex_tanques = re.compile(
        r"(-?\d{1,3}(?:\.\d{3})*,\d{3})\s+"  # Perdas/Sobras
        r"(\d{1,3}(?:\.\d{3})*,\d{3})\s+"    # Estoque Fechamento
        r"(\d{1,3}(?:\.\d{3})*,\d{3})\s+"    # Vendas
        r"(?:(\d{1,3}(?:\.\d{3})*,\d{3})\s+)?"+  # Recebimentos (opcional)
        r"(\d{1,3}(?:\.\d{3})*,\d{3})\s+"    # Estoque Abertura
        r"([A-Z\s\d]+?)\s+"                  # Item (texto pode conter espaços e números)
        r"(\d+)"                             # Tanque (número inteiro)
    )

    dados_tanques = []

    # Encontrar todas as correspondências usando a regex
    matches = regex_tanques.finditer(new_text)
    
    for match in matches:
        perdas_sobras, estoque_fechamento, vendas, recebimentos, estoque_abertura, item, tanque = match.groups()

        # Tratar o campo 'Recebimentos' como None se estiver ausente
        recebimentos = float(recebimentos.replace(".", "").replace(",", ".")) if recebimentos else 0
        
        dados_tanques.append({
            "type": "tanque",
            "tanque": int(tanque),
            "abertura": float(estoque_abertura.replace(".", "").replace(",", ".")),
            "fechamento": float(estoque_fechamento.replace(".", "").replace(",", ".")),
            "venda": float(vendas.replace(".", "").replace(",", ".")),
            "recebimento": recebimentos,
        })
    
    return dados_tanques


def get_data(cnpj, file_path):
    # Extração do texto
    lines = extract_text_from_pdf(file_path)

    # Extração dos dados
    bico_data = extract_bico_data(lines)
    tanque_data = extract_tanque_data(lines)

    bico_tanque_data = []
    for bico in bico_data:
        bico_tanque_data.append(bico)
    for tanque in tanque_data:
        bico_tanque_data.append(tanque)

    
    path_xlsx = f"output/{cnpj}.xlsx"
    path_dac = f"input/dac/{cnpj}.txt"
    return bico_tanque_data, cnpj, path_dac, path_xlsx