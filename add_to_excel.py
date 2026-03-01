import xlsxwriter
from main import get_book_links_generator, get_book_data
from urllib.parse import quote

search_query_1 = input('Какие книги ищем: ')
search_query = quote(search_query_1)
filename = input('Название документа: ')
print("Начинаем парсинг...")

links_gen = get_book_links_generator(search_query)
books_gen = get_book_data(links_gen)

workbook = xlsxwriter.Workbook(f'{filename}.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column("A:A", 20)
worksheet.set_column("B:B", 100)
worksheet.set_column("C:C", 100)

worksheet.write(0, 0, 'Автор')
worksheet.write(0, 1, 'Название')
worksheet.write(0, 2, 'Ссылка для скачивания')

row = 1
for author, title, download_link in books_gen:
    worksheet.write(row, 0, author)
    worksheet.write(row, 1, title)
    worksheet.write(row, 2, download_link)
    row += 1
    print(f"Записано: {author} - {title}")

if (row-1) == 0:
    print('Увы, книг с таким названием в источнике не найдено :(')
    workbook.close()
else:
    workbook.close()
    print(f"\nГотово! Записано книг: {row-1}")
    print(f"Файл сохранен как: {filename}.xlsx")