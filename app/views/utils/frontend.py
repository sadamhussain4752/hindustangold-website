
import locale
locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8') 

def indian_formatted_currency(amount):
    return locale.format('%d', amount, grouping=True)

