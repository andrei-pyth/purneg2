import re
import fitz
import os
from time import sleep

def grn_reg_date(text):
    res = re.search(r'ГРН и дата внесения в ЕГРЮЛ записи,\nсодержащей указанные сведения\n(.*)\n(.*)', text)
    if not res:
        res = re.search(r'ГРН и дата внесения записи в ЕГРЮЛ\n(.*)\n(.*)', text)
    return res.group(1), res.group(2)

def slt_jn(text):
    text = text.split('\n')
    return ' '.join(text)


def clean_text(text):

    ind = re.search('ГРН и дата', text)
    if ind:
        ind1 = ind.span()[0]
        text = text[:ind1]

    ind2 = re.search('Страница \d', text)
    if ind2:
        ind3 = ind2.span()[0]
        text = text[:ind3]

    ind4 = re.search('Сведения о свидетельстве, подтверждающем факт', text)
    if ind4:
        ind5 = ind4.span()[0]
        text = text[:ind5]

    txt = re.sub('\n\d+\n', '', text)

    txt = re.sub('Наименование документа', '', txt)

    txt = re.sub('ДОКУМЕНТ ОБ ОПЛАТЕ\nГОСУДАРСТВЕННОЙ ПОШЛИНЫНомер документа\d+\nДата документа\n.*\n', '', txt)
    return txt

def make_capitalize(text):
    text = text.split()
    text[0] = text[0].lower()
    try:
        text[1] = text[1].capitalize()
    except IndexError:
        print('Ошибка в форматировани заглавных букв текста. Печатаю как есть. Проверьте форматирование в документе!')
    return text

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
