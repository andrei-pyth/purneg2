import os
from time import sleep

def check_download(ext_ch):
    while True:
        filenames = os.listdir()
        if len(filenames) > 0 and not any('.crdownload' in name for name in filenames):
            break
    for name in filenames:
        if name.endswith('.crdownload'):
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
