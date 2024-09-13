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
    regex_dados = re.compile(r"(\d{3})\s+(\d{3})\s+([\w\s]+(?:\s[\w\s]+)*)\s+(\d{1,3}(?:\.\d{3})*,\d{3})\s+(\d{1,3}(?:\.\d{3})*,\d{3})\s+(\d{1,3}(?:\.\d{3})*,\d{3})\s+(\d{1,3}(?:\.\d{3})*,\d{3})\s+(\d{1,3}(?:\.\d{3})*,\d{3})")

    dados_extracao = []
    for linha in texto.split('\n'):
        linha = linha.strip()
        match_dados = regex_dados.match(linha)
        if match_dados:
            bomba, bico, produto, abertura, fechamento, sem_intervencao, com_intervencao, afericao = match_dados.groups()
            dados_extracao.append({
                "type": "bico",
                "bico": int(bico),
                "abertura": format_value(abertura),
                "fechamento": format_value(fechamento),
                "afericao": format_value(afericao),
                "venda": 0
            })

    return dados_extracao

def extract_tanque_data(texto):
    # Regex para extrair os dados da seção "movimentação por tanques"
    regex_mov_tanques = re.compile(r"(\d{3})\s+(\d{1,3}(?:\.\d{3})*,\d{3})\s+([\w\s]+)\s+(\d{1,3}(?:\.\d{3})*,\d{3})\s*(\d{1,3}(?:\.\d{3})*,\d{3})?\s*(-?\d{1,3}(?:\.\d{3})*,\d{3})")
    movimentacao_tanques = []
    for linha in texto.split('\n'):
        linha = linha.strip()
        match = regex_mov_tanques.match(linha)
        if match:
            tanque, estoque_abertura, produto, estoque_fechamento, recebimentos, falta = match.groups()
            movimentacao_tanques.append({
                "type": "tanque",
                "tanque": int(tanque),
                "abertura": format_value(estoque_abertura),
                "fechamento": format_value(estoque_fechamento),
                "recebimento": format_value(recebimentos),
                "venda": 0

            })

    return movimentacao_tanques


def get_data(cnpj, file_path):
    # Extração do texto
    texto = extract_text_from_pdf(file_path)

    # Extração dos dados
    bico_data = extract_bico_data(texto)
    tanque_data = extract_tanque_data(texto)
    bico_tanque_data = []
    for bico in bico_data:
        bico_tanque_data.append(bico)
    for tanque in tanque_data:
        bico_tanque_data.append(tanque)

    path_xlsx = f"output/{cnpj}.xlsx"
    path_dac = f"input/dac/{cnpj}.txt"
    return bico_tanque_data, cnpj, path_dac, path_xlsx

