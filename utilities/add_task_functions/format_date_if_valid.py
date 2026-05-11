from dateutil.parser import parse
import pandas as pd

def format_date_if_valid(value):
    try:
        if pd.isna(value) or value == "":
            return ""
        if isinstance(value, str):
            value = parse(value)
        return value.strftime('%d %B %Y')
    except Exception as e:
        print(f"⚠️ Date formatting failed for {value}: {e}")
        return ""
