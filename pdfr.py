import os
import fitz
import re
import get_egrul
import file_orgzer
from time import sleep


class EgrulData:
    def __init__(self):
        self.text = self.get_text()
        self.okveds = self.get_okved(self.text)
        self.full_name = re.search(r'Настоящая выписка содержит сведения о юридическом лице\n(.*)', self.text).group(1)
        self.ogrn = re.search(r'ОГРН(.*)', self.text).group(1)
        self.name_grn = self.grn_reg_date(self.text)[0]
        self.name_reg_date = self.grn_reg_date(self.text)[1]
        self.short_name = re.search(r'Сокращенное наименование на русском\nязыке\n(.*)', self.text).group(1)
        self.location_adress = Location(self.text)
        self.creation_method = re.search(r'Способ образования\n(.*)', self.text).group(1)
        self.reg_date = re.search(r'Дата регистрации\n(.*)', self.text).group(1)
        self.chefs = Chefs(self.text)
        self.capital = Capital(self.text)
        self.inn = self.get_inn(self.text)
        self.kpp = self.get_kpp(self.text)

    def get_kpp(text):
        res = re.search(r'КПП юридического лица\n(.*)', text).group(1)
        return res

    def get_inn(text):
        res = re.search(r'ИНН юридического лица\n(.*)', text).group(1)
        return res

    def grn_reg_date(self, text):
        res = re.search(r'ГРН и дата внесения в ЕГРЮЛ записи,\nсодержащей указанные сведения\n(.*)\n(.*)', text)
        return res.group(1), res.group(2)

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

class Location(EgrulData):
    def __init__(self, text):
        self.text = get_text(r'Место нахождения и адрес юридического лица\n', text)
        self.region = LocationRegion(self.text)
        self.address = LocationAddress(self.text)

class LocationRegion(Location):
    def __init__(self, text):
        self.region_name = re.search(r'Место нахождения юридического лица\n(.*)', text).group(1)
        self.grn, self.reg_date = EgrulData.grn_reg_date(self, text)

class LocationAddress(Location):
    def __init__(self, text):
        self.text = get_text(r'Адрес юридического лица\n', text)
        self.address = re.search(r'Адрес юридического лица\n(.*\n){5}', text).group(0).split('\n')
        self.address = self.address[1:-1]
        print(self.address)
        self.index, self.city, self.street, self.building, *self.appartment = self.address
        self.grn, self.reg_date = EgrulData.grn_reg_date(self, self.text)

class Chefs(EgrulData):
    def __init__(self, text):
        self.text = get_text(r'Сведения о лице, имеющем право без доверенности действовать от имени юридического\nлица', text)
        self.person = re.search(r'Фамилия\nИмя\nОтчество\n(.*\n){3}', self.text).group(0).split('\n')
        self.person = self.person[3:-1]
        print(self.person)
        self.surname, self.name, self.paternal = self.person
        self.inn = re.search(r'ИНН\n(.*)', self.text).group(1)
        self.grn, self.reg_date = EgrulData.grn_reg_date(self, self.text)
        self.post = Post(self.text)

class Post(Chefs):
    def __init__(self, text):
        self.text = get_text(r'Должность\n(.*)', text)
        self.post_name = re.search(r'Должность\n(.*)', text).group(1)
        self.grn, self.reg_date = EgrulData.grn_reg_date(self, self.text)

class Capital(EgrulData):
    def __init__(self, text):
        self.text = get_text(r'Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде\n', text)
        self.type = re.search(r'Вид\n(.*)', self.text).group(1)
        print(self.type, '====> Данные о виде капитала получены')
        print(self.text)
        self.amount = re.search(r'Размер \(в рублях\)\n(.*)', self.text).group(1)
        print(self.amount)
        self.grn, self.reg_date = EgrulData.grn_reg_date(self, self.text)

def get_text(pattern, text):
    res = re.search(pattern, text)
    return text[res.span()[1]:]


def main():
    get_egrul.main()
    file_orgzer.org_files('pdf_files', '.pdf', 'pdf_files/egrul.pdf', 'ЕГРЮЛ')
    res = EgrulData()
    return res

if __name__ == '__main__':
    main()





