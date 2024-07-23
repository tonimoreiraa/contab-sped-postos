import re

# Exemplo de texto
text = """
(Seu texto aqui)
"""

# Regex para cada item
regex_patterns = {
    "Produto": r" -\s*(.*?)\s*2\) D\. Inicial",
    "Estoque de Abertura": r"3\.1\)\s*Estoque de Abertura\s*([\d.,]+)",
    "Volume Recebido": r"4\.3\)\s*Total Recebido\s*([\d.,]+)",
    "Tanque": r"5\.6\)\s*-\s*Vendas Bico\s*([\d.,]+)",
    "Bico": r"5\.6\)\s*-\s*Vendas Bico\s*[\d.,]+\s*([\d.,]+)",
    "Fechamento": r"5\.6\)\s*-\s*Vendas Bico\s*[\d.,]+\s*[\d.,]+\s*([\d.,]+)",
    "Abertura": r"5\.6\)\s*-\s*Vendas Bico\s*[\d.,]+\s*[\d.,]+\s*[\d.,]+\s*([\d.,]+)",
    "Aferições": r"5\.6\)\s*-\s*Vendas Bico\s*[\d.,]+\s*[\d.,]+\s*[\d.,]+\s*[\d.,]+\s*([\d.,]+)",
    "Venda Bico": r"5\.6\)\s*-\s*Vendas Bico\s*[\d.,]+\s*[\d.,]+\s*[\d.,]+\s*[\d.,]+\s*[\d.,]+\s*([\d.,]+)",
    "Perdas": r"8\)\s*Perdas e Sobras\s*([\d.,]+)",
    "Estoque de Fechamento": r"7\)\s*Estoque de Fechamento\s*([\d.,]+)"
}

# Função para extrair dados
def extract_info(text, pattern):
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).replace('.', '').replace(',', '.') if match else None

# Extraindo informações
extracted_data = {key: extract_info(text, pattern) for key, pattern in regex_patterns.items()}

# Mostrando resultados
for key, value in extracted_data.items():
    print(f"{key}: {value}")
