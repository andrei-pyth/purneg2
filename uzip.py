from zipfile import ZipFile

def main():
    with ZipFile('zip_files/srn.zip') as zf:
        lst = zf.namelist()
        for count, item in enumerate(lst):
            with zf.open(item) as file:
                pg = file.read()
                pg = pg.decode('utf-8')
            yield pg
