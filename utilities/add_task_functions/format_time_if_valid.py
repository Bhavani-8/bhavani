from datetime import datetime, time as dt_time
import pandas as pd


# def format_time_if_valid(value):
#     print(f"[format_time_if_valid] Received value: {repr(value)}")
#     if pd.isnull(value) or value == "":
#         print("[format_time_if_valid] Value is null or empty; returning None.")
#         return None
#     try:
#         # Determine type and convert accordingly
#         if isinstance(value, (pd.Timestamp, datetime)):
#             print("[format_time_if_valid] Detected pandas Timestamp / datetime.")
#             time_obj = value.time()
#         elif isinstance(value, dt_time):
#             print("[format_time_if_valid] Detected time object.")
#             time_obj = value
#         elif isinstance(value, str):
#             cleaned = value.strip()
#             print(f"[format_time_if_valid] Detected string. Cleaned value: {repr(cleaned)}. Parsing with format '%I:%M %p'.")
#             time_obj = pd.to_datetime(cleaned, format='%I:%M %p').time()
#         else:
#             print(f"[format_time_if_valid] Detected other type ({type(value)}). Attempting generic parse.")
#             time_obj = pd.to_datetime(value).time()

#         formatted = time_obj.strftime('%I:%M %p')
#         print(f"[format_time_if_valid] Parsed time object: {time_obj}. Formatted result: {formatted}")
#         return formatted
#     except Exception as e:
#         print(f"[format_time_if_valid] ⚠️ Could not convert time: {repr(value)} — {e}")
#         return None
    
def format_time_if_valid(value):
    print(f"[format_time_if_valid] Received value: {repr(value)}")

    # 🔹 Case 1: Empty or null
    if value is None or value == "" or (isinstance(value, float) and pd.isna(value)):
        print("[format_time_if_valid] Value is null or empty; returning None.")
        return None

    try:
        # 🔹 Case 2: Pandas Timestamp or datetime
        if isinstance(value, (pd.Timestamp, datetime)):
            print("[format_time_if_valid] Detected pandas Timestamp or datetime.")
            time_obj = value.time()

        # 🔹 Case 3: Already datetime.time
        elif isinstance(value, dt_time):
            print("[format_time_if_valid] Detected time object.")
            time_obj = value

        # 🔹 Case 4: String time
        elif isinstance(value, str):
            cleaned = value.strip()
            print(f"[format_time_if_valid] Detected string. Cleaned: {repr(cleaned)}")

            if cleaned == "":
                print("[format_time_if_valid] Empty string after clean; returning None.")
                return None

            # Try parsing 12-hour format first: "09:30 AM"
            try:
                time_obj = pd.to_datetime(cleaned, format='%I:%M %p').time()
            except:
                # Try automatic parsing
                time_obj = pd.to_datetime(cleaned).time()

        # 🔹 Case 5: Anything else
        else:
            print(f"[format_time_if_valid] Detected {type(value)} → trying generic parse.")
            time_obj = pd.to_datetime(value).time()

        formatted = time_obj.strftime('%I:%M %p')
        print(f"[format_time_if_valid] Parsed time object → Final: {formatted}")
        return formatted

    except Exception as e:
        print(f"[format_time_if_valid] ⚠️ Error converting {repr(value)} — {e}")
        return None
