import PyPDF2
import re
from format_value import format_value

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        texto = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            texto += page.extract_text()
    return texto

def extract_bico_data(texto):
    # Regex para extrair os dados dos bicos e tanques
    regex_dados = re.compile(r"(\d+)\s+(\d+)\s+(\d+)\s+(.+?)\s+(\d{1,3}(?:\.\d{3})*,\d+)\s+(\d{1,3}(?:\.\d{3})*,\d+)\s+(\d{1,3}(?:\.\d{3})*,\d+)\s+(\d{1,3}(?:\.\d{3})*,\d+)\s+(\d{1,3}(?:\.\d{3})*,\d+)")

    dados_extracao = []
    for linha in texto.split('\n'):
        linha = linha.strip()
        match_dados = regex_dados.match(linha)
        if match_dados:
            bomba, bico, tanque, produto, abertura, fechamento, sem_intervencao, com_intervencao, afericao = match_dados.groups()
            dados_extracao.append({
                "type": "bico",
                "bico": bico,
                "abertura": format_value(abertura),
                "fechamento": format_value(fechamento),
                "afericao": format_value(afericao),
                "venda": 0
            })

    return dados_extracao

def extract_tanque_data(texto):
    # Regex para extrair os dados da seção "movimentação por tanques"
    regex_mov_tanques = re.compile(
        r"^(\d+)\s+"  # Tanque
        r"([A-Z\s\-0-9]+?)\s+"  # Item (ajustado para letras maiúsculas, espaços e hífens)
        r"(\d{1,3}(?:\.\d{3})*,\d{3})\s+"  # Capacidade
        r"(\d{1,3}(?:\.\d{3})*,\d{3})\s+"  # Estoque Abertura
        r"(\d{1,3}(?:\.\d{3})*,\d{3})\s+"  # Recebimentos
        r"(\d{1,3}(?:\.\d{3})*,\d{3})\s+"  # Vendas
        r"(-?\d{1,3}(?:\.\d{3})*,\d{3})\s+"  # Estoque Fechamento
        r"(-?\d{1,3}(?:\.\d{3})*,\d{3})\s+"  # Campo adicional 1
        r"(-?\d{1,3}(?:\.\d{3})*,\d{2})$"  # Campo adicional 2 (ajustado para duas casas decimais)
    )
    movimentacao_tanques = []
    for linha in texto.split('\n'):
        linha = linha.strip()
        match = regex_mov_tanques.match(linha)
        if match:
            tanque, produto, estoque_abertura, recebimentos, vendas, estoque_fechamento, campo, campo_adicional_1, campo_adicional_2 = match.groups()
            movimentacao_tanques.append({
                "type": "tanque",
                "tanque": tanque,
                "abertura": format_value(estoque_abertura),
                "fechamento": format_value(estoque_fechamento),
                "recebimento": format_value(recebimentos),
                "venda":format_value(vendas)
            })

    return movimentacao_tanques

def get_data(cnpj, file_path):

    # Extração do texto
    text = extract_text_from_pdf(file_path)

    # Extração dos dados
    bico_data = extract_bico_data(text)
    tanque_data = extract_tanque_data(text)
    bico_tanque_data = []
    for bico in bico_data:
        bico_tanque_data.append(bico)
        
    for tanque in tanque_data:
        bico_tanque_data.append(tanque)

    path_xlsx = f"output/{cnpj}.xlsx"
    path_dac = f"input/dac/{cnpj}.txt"
    return bico_tanque_data, cnpj, path_dac, path_xlsx
