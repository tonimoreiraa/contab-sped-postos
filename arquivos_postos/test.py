import re

def test(text):
    data = []

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

    # Agrupando os dados
    for i in range(len(produtos)):
        info = {
            "Produto": produtos[i],
            "Estoque de Abertura": estoques_abertura[i] if i < len(estoques_abertura) else "N/A",
            "Volume Recebido": volumes_recebidos[i] if i < len(volumes_recebidos) else "N/A",
            "Tanque": vendas_bico[i][0] if i < len(vendas_bico) else "N/A",
            "Bico": vendas_bico[i][1] if i < len(vendas_bico) else "N/A",
            "Fechamento": vendas_bico[i][2] if i < len(vendas_bico) else "N/A",
            "Abertura": vendas_bico[i][3] if i < len(vendas_bico) else "N/A",
            "Aferições": vendas_bico[i][4] if i < len(vendas_bico) else "N/A",
            "Venda Bico": vendas_bico[i][5] if i < len(vendas_bico) else "N/A",
            "Perdas": perdas[i] if i < len(perdas) else "N/A",
            "Estoque de Fechamento": estoques_fechamento[i] if i < len(estoques_fechamento) else "N/A"
        }
        data.append(info)

    for item in data:
        print(item)

    return data


