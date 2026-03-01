import requests
from bs4 import BeautifulSoup
from time import sleep
import re

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def get_book_links_generator(search_query):
    """Генератор: Находим ссылки на всех страницах"""
    url = f'https://m.flibusta.is/booksearch?ask={search_query}'
    response = requests.get(url, headers=headers)
    sleep(2)
    soup = BeautifulSoup(response.text, 'lxml')

    total_pages = 1
    item_list = soup.find('div', class_ = 'item-list')
    if item_list:
        li_items = item_list.find_all('li', class_ = 'pager-item')
        if li_items:
            last_page = li_items[-1].find('a')
            if last_page:
                total_pages = int(last_page.text)
                print(f'Страниц найдено: {total_pages}')
    for page in range(total_pages):
        print(f"Парсим страницу №{page+1} из {total_pages}")
        if page == 0:
            current_soup = soup
        else:
            page_url = f'https://m.flibusta.is/booksearch?page={page}&ask={search_query}'
            response = requests.get(page_url, headers=headers)
            sleep(2)
            current_soup = BeautifulSoup(response.text, 'lxml')

        for li in current_soup.find_all('li'):
            book_link = li.find('a', href=lambda x: x and x.startswith('/b/'))
            if book_link:
                yield book_link['href']

def get_book_data(book_links_generator):
    """Генератор: Получаем всю информацию по книге"""
    for link in book_links_generator:
        print("Собираем информацию со страницы книги...")
        book_url = f'https://m.flibusta.is{link}'
        sleep(2)
        response = requests.get(book_url, headers=headers)
        soup_book = BeautifulSoup(response.text, 'lxml')

        author_find = soup_book.find('a', href=re.compile(r'^/a/\d+$'))
        author = author_find.text if author_find else 'Автор не найден :('

        title_find = soup_book.find('h1', class_ = 'title')
        title = title_find.text if title_find else 'Название не найдено :('

        download_link = f'https://m.flibusta.is{link}/download'

        yield author, title, download_link








