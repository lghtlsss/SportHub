from requests import get


def check_image(post_id) -> bool:
    """Проверяет, есть ли картинка по этому адресу"""
    response = get(f'http://localhost:8070/api/images/{post_id}')
    if response.content:
        return True
    return False
