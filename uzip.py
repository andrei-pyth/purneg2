from zipfile import ZipFile
from zipfile import BadZipFile

def main(file_name):
    try:
        with ZipFile(f'zip_files/{file_name}') as zf:
            lst = zf.namelist()
            print('Скачано {} файлов...'.format(len(lst)))
            print('Происходит поочередная проверка файлов архива предприятий с СРН...')
            for count, item in enumerate(lst):
                with zf.open(item) as file:
                    print(f'Файл №{count}')
                    pg = file.read()
                    pg = pg.decode('utf-8')
                    yield pg
    except BadZipFile:
        yield
