from zipfile import ZipFile
import os

def main():
    if not os.path.isdir('xml_files'):
        os.mkdir('xml_files')
    with ZipFile('zip_files/srn.zip') as zf:
        lst = zf.namelist()
        for count, item in enumerate(lst):
            zf.open(item)


            print(f'Распаковано {count} файлов из базы СРН')
            
