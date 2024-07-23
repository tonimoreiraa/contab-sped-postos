import re
import PyPDF2

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

    # Dividir o texto por produtos
    produtos = re.split(r' - ', text)[1:]

    print("Número de produtos encontrados:", len(produtos))

    for produto in produtos:
        print("\nProcessando produto:\n", produto[:500])  # Print dos primeiros 500 caracteres do produto

        produto_nome = re.search(r'(.+?)\s+2\) D\. Inicial', produto)
        if produto_nome:
            produto_nome = produto_nome.group(1).strip()
        else:
            produto_nome = "N/A"
        
        print("Produto:", produto_nome)

        # Extração de informações de Tanque
        tanque_info = {
            "Produto": produto_nome,
            "Tanque": re.search(r'TQ\s*(\d+)', produto).group(1) if re.search(r'TQ\s*(\d+)', produto) else "N/A",
            "Abertura": re.search(r'3\.1\) Estoque de Abertura\s+([\d.,]+)', produto).group(1).replace('.', '').replace(',', '.') if re.search(r'3\.1\) Estoque de Abertura\s+([\d.,]+)', produto) else "N/A",
            "Fechamento": re.search(r'7\) Estoque de Fechamento\s+([\d.,]+)', produto).group(1).replace('.', '').replace(',', '.') if re.search(r'7\) Estoque de Fechamento\s+([\d.,]+)', produto) else "N/A",
            "Recebimento": re.search(r'4\.3\) Total Recebido\s+([\d.,]+)', produto).group(1).replace('.', '').replace(',', '.') if re.search(r'4\.3\) Total Recebido\s+([\d.,]+)', produto) else "N/A"
        }
        print("Tanque info:", tanque_info)
        data_tanque.append(tanque_info)

        # Extração de informações de Bico
        bico_matches = re.findall(r'5\.6\) - Vendas Bico\s+(\d+)\s+(\d+)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)', produto)
        print("Bico matches encontrados:", bico_matches)

        for match in bico_matches:
            bico_info = {
                "Bico": match[1],
                "Tanque": match[0],
                "Fechamento": match[2].replace('.', '').replace(',', '.'),
                "Abertura": match[3].replace('.', '').replace(',', '.'),
                "Afericao": match[4].replace('.', '').replace(',', '.'),
                "VendaBico": match[5].replace('.', '').replace(',', '.')
            }
            print("Bico info:", bico_info)
            data_bico.append(bico_info)

        # Capturando vendas adicionais
        vendas_bico_extras_pattern = r'5\s+(\d+)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)'
        vendas_bico_extras_data = re.findall(vendas_bico_extras_pattern, produto)

        print("Vendas bico extras encontrados:", vendas_bico_extras_data)

        for extra in vendas_bico_extras_data:
            extra_info = {
                "Bico": extra[0],
                "Tanque": extra[1],
                "Fechamento": extra[2].replace('.', '').replace(',', '.'),
                "Abertura": extra[3].replace('.', '').replace(',', '.'),
                "Afericao": extra[4].replace('.', '').replace(',', '.'),
                "VendaBico": extra[5].replace('.', '').replace(',', '.')
            }
            print("Extra bico info:", extra_info)
            data_bico.append(extra_info)

    return data_tanque, data_bico

# Caminho para o PDF
pdf_path = "input/relatorio/25023880000142.pdf"

# Extraindo texto do PDF
pdf_text = extract_text_from_pdf(pdf_path)

# Exibindo o texto extraído para análise
print("Texto extraído do PDF:")
print(pdf_text[:2000])  # Print dos primeiros 2000 caracteres do texto extraído

# Extraindo dados do texto
data_tanque, data_bico = extract_data(pdf_text)

# Exibindo os dados extraídos
print("\nDados de Tanque:")
for tanque in data_tanque:
    print(tanque)

print("\nDados de Bico:")
for bico in data_bico:
    print(bico)
