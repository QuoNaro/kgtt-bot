from datetime import datetime
from ruobr_student import RuobrCookies, AuthorizationError

def validate(date_str : str , format : str) -> bool:
    "Проверка строки на соответствие формату даты"
    try:
        result = bool(datetime.strptime(date_str, format))
    except ValueError:
        result = False
    return result


def check_ruobr_auth(login : str, password : str) -> bool:
    try:
        RuobrCookies(login,password)
        return True
    except Exception:
        return False