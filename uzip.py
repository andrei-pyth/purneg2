import os
from time import sleep
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
            zf = ZipFile(item, 'r')
    lst1 = zf.namelist()
    for item1 in lst1:
        if '.pdf' in item1:
            fl = item1
    zf.extract(fl, 'pdf_files/')
    os.rename(f'pdf_files/{fl}', 'pdf_files/blocks.pdf')
