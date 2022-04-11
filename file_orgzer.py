import re
import fitz
import os
from time import sleep

def get_text(pattern, text):
    res = re.search(pattern, text)
    if res:
        return text[res.span()[1]:]
    else:
        return

def get_text_main(file):
    with fitz.open(f'pdf_files/{file}.pdf') as doc:
        txt = ''
        for page in doc.pages():
            txt += page.get_text()
    return txt

def check_download(ext_ch):
    while True:
        filenames = os.listdir()
        print(f'Происходит скачивание архива {filenames}...')
        sleep(1)
        if len(filenames) > 0 and not any('.tmp' in name for name in filenames):
            break
    for name in filenames:
        if name.endswith('.tmp'):
            continue
        if name.endswith(ext_ch) or name.endswith(ext_ch.upper()):
            print('')
            print('Download complete.')
            print('')
            break
        else:
            break

def org_files(dir_n, ext, new_name, type_n):
    if not os.path.isdir(dir_n):
        os.mkdir(dir_n)
    lst = os.listdir()
    for item in lst:
        if ext in item or ext.upper() in item:
            os.rename(item, new_name)
            print(f'Выписка {type_n} переименована и сохранена в общую папку')
    sleep(2)
