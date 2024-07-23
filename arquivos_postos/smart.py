import PyPDF2
import re
from test import test

cnpj = "25023880000142"
empresa = "AUTO POSTO SMART LTDA  EPP"

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        texto = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            texto += page.extract_text()
    return texto

def extract_tanque_bico_data(texto):
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
                "Abertura": abertura,
                "Fechamento": fechamento
            })
        

    return dados_extracao

def extract_movimentacao_por_tanques(texto):
    # Regex para extrair os dados da seção "movimentação por tanques"
    regex_mov_tanques = re.compile(r"(\d+)([\w\s-]+)\s+([\d\.,]+)\s+([\d\.,]+)\s+([\d\.,]+)\s+([\d\.,-]+)\s+([\w\s]+)")

    movimentacao_tanques = []
    for linha in texto.split('\n'):
        linha = linha.strip()
        match = regex_mov_tanques.match(linha)
        if match:
            tanque, combustivel, estoque_abertura, estoque_fechamento, recebimentos, falta, sigla = match.groups()
            movimentacao_tanques.append({
                "Tanque": tanque,
                "Abertura": estoque_abertura,
                "Fechamento": estoque_fechamento,
                "Recebimento": recebimentos
            })
        

    return movimentacao_tanques


try:
    file_path = f"input/relatorio/{cnpj}.pdf"
except:
    file_path = f"input/relatorio/{cnpj}.xlsx"

# Extração do texto
texto = extract_text_from_pdf(file_path)
#print(texto)
test(texto)

# Extração dos dados
bico_data = extract_tanque_bico_data(texto)
tanque_data = extract_movimentacao_por_tanques(texto)

bico = {}
for data in bico_data:
    bico[data['Bico']] = [data['Abertura'], data['Fechamento']]
tanque = {}
for data in tanque_data:
    tanque[data['Tanque']] = [data['Abertura'], data['Fechamento'], data['Recebimento']]

print(bico)
print(tanque)
