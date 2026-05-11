from dateutil import parser

def normalize_day_and_month(date_str):
    try:
        parsed_date = parser.parse(date_str, dayfirst=True)  # Handles DD-MM-YYYY, MM/DD/YYYY, etc.
        # Format 1: Full date in YYYY-MM-DD
        day_num = parsed_date.strftime("%d")
        # Format 2: Month name
        month_name = parsed_date.strftime("%B")
        return day_num, month_name.capitalize()
    except Exception:
        return None, None