from dateutil import parser

def normalize_date(date_str):
    try:
        parsed_date = parser.parse(date_str, dayfirst=True)  # dayfirst=True handles DD-MM-YYYY automatically
        return parsed_date.strftime("%d %B %Y")
    except Exception:
        return None