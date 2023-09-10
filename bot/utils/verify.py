from datetime import datetime

def validate(date_str : str , format : str) -> bool:
    "Проверка строки на соответствие формату даты"
    try:
        result = bool(datetime.strptime(date_str, format))
    except ValueError:
        result = False
    return result
