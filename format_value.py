def format_value(value):
    try:
        value = str(value)
        value = value.replace('.', '').strip()
        value = value.replace(',', '.')
        # Converter para float e formatar com duas casas decimais
        value_float = float(value)
        #value_formated = "{:.2f}".format(value_float)
        #value_formated = value_formated.replace('.', ',')
        return value_float
    except ValueError:
        try:
            return float(value)
        except Exception as e :
            print(f"Problema encontrado ao executar 'format_value.py': {e}")
            return 0