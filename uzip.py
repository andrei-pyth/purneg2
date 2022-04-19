from zipfile import ZipFile
from zipfile import BadZipFile

def main():
    try:
        with ZipFile('zip_files/srn.zip') as zf:
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
