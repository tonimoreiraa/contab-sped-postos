import os
from PyPDF2 import PdfReader
from openpyxl import load_workbook

def identify_report_model(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.pdf':
        reader = PdfReader(file_path)

        reader.stream.seek(0)
        doc_info = {
            'title': reader.metadata.get('/Title', ''),
            'subject': reader.metadata.get('/Subject', ''),
            'author': reader.metadata.get('/Author', ''),
            'producer': reader.metadata.get('/Producer', '')
        }

        if doc_info['subject'] == 'FastReport PDF export' and doc_info['author'] == 'FastReport':
            return 'A'
        
        if doc_info['title'] == 'Relatório AutoSystem PRO' or doc_info['producer'] == 'Microsoft: Print To PDF':
            return 'B'
        
        if doc_info['title'] == 'Declaração de Atividades do Contribuinte' and doc_info['subject'] == 'Exportação para PDF':
            return 'C'
        
        if 'JasperReports' in reader.metadata.get('/Creator', ''):
            return 'D'
        
        reader.stream.seek(0)
        version = reader.stream.readline().decode('utf-8', errors='ignore')
        
        if '1.4' in version:
            return 'I'

        if not doc_info['author'] and not doc_info['subject']:
            return 'E'
        
    
    elif file_extension == '.xlsx':
        workbook = load_workbook(file_path)
        sheet = workbook.active
        cell_a1 = sheet['A1'].value

        if cell_a1 == 'INFORMAÇÕES MENSAIS DE ENCERRANTES DE COMBUSTÍVEIS':
            return 'F'
        
        if cell_a1 == 'RELATORIO PARA APRESENTAR - DAC':
            return 'G'
        
        if 'DATA INICIAL' in cell_a1:
            return 'H'

    return 'Modelo desconhecido'