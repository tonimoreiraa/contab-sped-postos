import PyPDF2
import re
from save_to_sheet import save_to_sheet

cnpj = "21309025000141"
empresa = "AUTO POSTO BRISA DO LAGO COMBUSTIVEIS E TRANSPORTES LTDA"

def get_data():
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
                    "Bico": bico,
                    "Produto": produto,
                    "Abertura": abertura,
                    "Fechamento": fechamento,
                    "Sem_intervencao": sem_intervencao,
                    "Com_intervencao": com_intervencao,
                    "Afericao": afericao
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
                tanque, produto, estoque_abertura, recebimentos, capacidade, estoque_fechamento, vendas, campo_adicional_1, campo_adicional_2 = match.groups()
                movimentacao_tanques.append({
                    "Tanque": tanque,
                    "Produto": produto,
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
    text = extract_text_from_pdf(file_path)

    # Extração dos dados
    bico_data = extract_bico_data(text)
    tanque_data = extract_tanque_data(text)

    save_to_sheet(bico_data, tanque_data, f"output/{cnpj}.xlsx")
    path_dac = f"input/dac/{cnpj}.txt"
    return bico_data, tanque_data, empresa, path_dac
