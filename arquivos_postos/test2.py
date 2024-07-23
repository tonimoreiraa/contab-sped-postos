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

    # Padrões regex para cada campo
    produto_pattern = r"-\s*(.+?)\s*2\) D\. Inicial"
    estoque_abertura_pattern = r"3\.1\) Estoque de Abertura\s+([\d.,]+)"
    volume_recebido_pattern = r"4\.3\) Total Recebido\s+([\d.,]+)"
    vendas_bico_pattern = r"5\.6\) - Vendas Bico\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)"
    perdas_pattern = r"8\) Perdas e Sobras\s+([\d.,-]+)"
    estoque_fechamento_pattern = r"7\) Estoque de Fechamento\s+([\d.,]+)"

    # Encontrando todas as ocorrências de cada campo
    produtos = re.findall(produto_pattern, text)
    estoques_abertura = re.findall(estoque_abertura_pattern, text)
    volumes_recebidos = re.findall(volume_recebido_pattern, text)
    vendas_bico = re.findall(vendas_bico_pattern, text)
    perdas = re.findall(perdas_pattern, text)
    estoques_fechamento = re.findall(estoque_fechamento_pattern, text)

    # Verificando se todos os campos foram encontrados
    print(f"Produtos encontrados: {produtos}")
    print(f"Estoques de Abertura encontrados: {estoques_abertura}")
    print(f"Volumes Recebidos encontrados: {volumes_recebidos}")
    print(f"Vendas Bico encontradas: {vendas_bico}")
    print(f"Perdas encontradas: {perdas}")
    print(f"Estoques de Fechamento encontrados: {estoques_fechamento}")

    # Agrupando os dados de Tanque
    for i in range(len(produtos)):
        tanque_info = {
            "Produto": produtos[i],
            "Estoque de Abertura": estoques_abertura[i] if i < len(estoques_abertura) else "N/A",
            "Volume Recebido": volumes_recebidos[i] if i < len(volumes_recebidos) else "N/A",
            "Estoque de Fechamento": estoques_fechamento[i] if i < len(estoques_fechamento) else "N/A"
        }
        print("Tanque info:", tanque_info)
        data_tanque.append(tanque_info)

    # Agrupando os dados de Bico
    for match in vendas_bico:
        bico_info = {
            "Tanque": match[0],
            "Bico": match[1],
            "Fechamento": match[2].replace('.', '').replace(',', '.'),
            "Abertura": match[3].replace('.', '').replace(',', '.'),
            "Afericao": match[4].replace('.', '').replace(',', '.'),
            "VendaBico": match[5].replace('.', '').replace(',', '.')
        }
        print("Bico info:", bico_info)
        data_bico.append(bico_info)

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
