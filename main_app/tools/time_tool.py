from datetime import datetime


def get_delta(input_time: datetime) -> str:
    """Считает разницу между переданным временем и текущем временем и возвращает правильную строку"""
    delta = datetime.now() - input_time
    seconds = int(delta.total_seconds())
    if seconds < 60:
        str_delta = f"{seconds} сек назад"
    elif seconds < 3600:
        str_delta = f"{seconds // 60} мин назад"
    elif seconds < 86400:
        str_delta = f"{seconds // 3600} ч назад"
    else:
        str_delta = f"{seconds // 86400} д назад"
    return str_delta
