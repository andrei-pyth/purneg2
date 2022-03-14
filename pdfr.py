import os
import fitz
import re
import get_egrul


class EgrulData:
    def __init__(self):
        self._text = self.get_text()
        self.okveds = self.get_okved(self._text)
        self.full_name = self.get_full_name(self._text)
        #self.write_txt(self._text)

    def get_full_name(self, text):
        res = re.search(r'Настоящая выписка содержит сведения о юридическом лице\n(.*)полное наименование юридического лица', text)
        print(res)

    def get_okved(self, text):
        lst = []
        text1 = text.split('Код и наименование вида деятельности')
        text1.pop(0)
        for item in text1:
            el = item.split('\n')
            res = self.get_sep_okveds(el)
            if res:
                lst.append(res)
        return lst

    def get_sep_okveds(self, item):
        txt = ''
        item.pop(0)
        for it in item:
            if it.isdigit():
                return txt
            else:
                txt += f'{it} '

    def get_text(self):
        with fitz.open('pdf_files/egrul.pdf') as doc:
            txt = ''
            for page in doc.pages():
                txt += page.get_text()
        return txt

    def write_txt(self, text):
        with open('text5.txt', 'w') as fl:
            fl.write(text)

def main():
    get_egrul.main()
    if not os.path.isdir('pdf_files'):
        os.mkdir('pdf_files')
    lst = os.listdir()
    for item in lst:
        if '.pdf' in item or '.PDF' in item:
            os.rename(item, 'pdf_files/egrul.pdf')
            print('Выписка ЕГРЮЛ переименована и сохранена в общую папку')
    res = EgrulData()
    return res.okveds

if __name__ == '__main__':
    main()





