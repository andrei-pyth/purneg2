from zipfile import ZipFile

def main():
    with ZipFile('zip_files/srn.zip') as zf:
        lst = zf.namelist()
        print('Скачано {} файлов...'.format(len(lst)))
        for count, item in enumerate(lst):
            print(f'Проверяется файл №{count}...')
            with zf.open(item) as file:
                pg = file.read()
                pg = pg.decode('utf-8')
            yield pg
