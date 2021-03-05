def format_number(number):
    number = str(number)[::-1]
    formatted = ''

    for idx, digit in enumerate(number):
        formatted += digit

        if ((idx+1)%3) == 0:
            formatted += ','
    
    if formatted.endswith(','):
        formatted = formatted[:-1]
    
    return formatted[::-1]