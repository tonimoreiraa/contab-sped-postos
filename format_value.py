def format_value(value):
    try:
        value = str(value)
        value = value.replace('.', '').strip()
        value = value.replace(',', '.')
        # Converter para float e formatar com duas casas decimais
        value_float = float(value)
        value_formated = "{:.2f}".format(value_float)
        #value_formated = value_formated.replace('.', ',')
        return float(value_formated)
    except ValueError:
        return value