import logging

from requests import RequestException
from bs4 import BeautifulSoup

from exceptions import ParserFindTagException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    """Перехват ошибки поиска тегов."""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def get_soup(session, url):
    """Получение объекта BeautifulSoup из URL-адреса."""
    response = session.get(url)
    if response.status_code != 200:
        logging.warning(f'Ошибка при получении страницы {url}')
        return None
    return BeautifulSoup(response.content, 'lxml')
