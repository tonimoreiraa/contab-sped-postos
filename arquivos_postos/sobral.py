import PyPDF2
import re
from save_to_sheet import save_to_sheet

cnpj = "03522014000163"
empresa = "SOBRAL COMERCIO E SERVICOS LTDA"

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
    regex_dados = re.compile(r"(\d+)\s+([\d\.,]+)\s+([\d\.,]+)\s+([\d\.,]+)\s+(\d+)\s+([\d\.,]+)\s+([\d\.,]+)")

    dados_extracao = []
    for linha in texto.split('\n'):
        linha = linha.strip()
        match_dados = regex_dados.match(linha)
        if match_dados:
            bico, abertura, fechamento, afericao, nserie, sem_intervencao,  com_intervencao = match_dados.groups()
            dados_extracao.append({
                "Bico": bico,
                "Produto": None, # to add
                "Abertura": abertura,
                "Fechamento": fechamento,
                "Sem_intervencao": sem_intervencao,
                "Com_intervencao": com_intervencao,
                "Afericao": afericao
            })

    return dados_extracao

def extract_tanque_data(texto):
    # Regex para extrair os dados da seção "movimentação por tanques"
    regex_mov_tanques = re.compile(r"(\d+)([\w\s-]+)\s+([\d\.,]+)\s+([\d\.,]+)\s+([\d\.,]+)\s+([\d\.,-]+)\s+([\w\s]+)")

    movimentacao_tanques = []
    for linha in texto.split('\n'):
        linha = linha.strip()
        match = regex_mov_tanques.match(linha)
        if match:
            tanque, produto, estoque_abertura, estoque_fechamento, recebimentos, falta, sigla = match.groups()
            try:
                estoque_abertura = int(estoque_abertura)
            except:
                pass
            movimentacao_tanques.append({
                "Tanque": tanque,
                "Produto": produto,
                "Abertura": estoque_abertura,
                "Fechamento": estoque_fechamento,
                "Recebimento": recebimentos
            })

    return movimentacao_tanques

def get_data():
    try:
        file_path = f"input/relatorio/{cnpj}.pdf"
    except:
        file_path = f"input/relatorio/{cnpj}.xlsx"

    # Extração do texto
    texto = extract_text_from_pdf(file_path)

    # Extração dos dados
    bico_data = extract_bico_data(texto)
    tanque_data = extract_tanque_data(texto)
    save_to_sheet(bico_data, tanque_data, f"output/{cnpj}.xlsx")
    path_dac = f"input/dac/{cnpj}.txt"
    return bico_data, tanque_data, empresa, path_dac
