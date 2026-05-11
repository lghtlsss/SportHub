from requests import get


def check_image(post_id):
    response = get(f'http://localhost:8070/api/images/{post_id}')
    if response.content:
        return True
    return False
