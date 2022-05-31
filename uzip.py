import os
from zipfile import ZipFile
from zipfile import BadZipFile

def main(file_name):
    try:
        with ZipFile(f'zip_files/{file_name}') as zf:
            lst = zf.namelist()
            for item in lst:
                with zf.open(item) as file:
                    pg = file.read()
                    pg = pg.decode('utf-8')
                    yield pg
    except BadZipFile:
        yield 'Bad zip-file'

def get_file_blocks():
    lst = os.listdir()
    for item in lst:
        if '.zip' in item:
            with ZipFile(item) as zf:
                lst = zf.namelist()
                for item1 in lst:
                    if '.pdf' or '.PDF' in item1:
                        zf.extract(item1, 'pdf_files/')
                        os.rename(f'pdf_files/{item1}', 'pdf_files/blocks.pdf')
