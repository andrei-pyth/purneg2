import re
import get_egrul
import file_orgzer
from file_orgzer import get_text


class EgrulData:
    def __init__(self):
        #get_egrul.main()
        #file_orgzer.org_files('pdf_files', '.pdf', 'pdf_files/egrul.pdf', 'ЕГРЮЛ')
        self.text = file_orgzer.get_text_main('egrul')
        self.okveds = self.get_okveds(self.text, 'Код и наименование вида деятельности', Okveds)
        self.full_name = re.search(r'Настоящая выписка содержит сведения о юридическом лице\n(.*)', self.text).group(1)
        self.ogrn = re.search(r'ОГРН(.*)', self.text).group(1)
        self.ogrn = self.ogrn.split()
        self.ogrn = ''.join(self.ogrn)
        self.name_grn = self.grn_reg_date(self.text)[0]
        self.name_reg_date = self.grn_reg_date(self.text)[1]
        self.short_name = re.search(r'Сокращенное наименование на русском\nязыке\n(.*)', self.text).group(1)
        self.location_adress = Location(self.text)
        self.creation_method = re.search(r'Способ образования\n(.*)', self.text).group(1)
        self.reg_date = self.get_reg_date(self.text)
        self.chefs = Chefs(self.text)
        self.founders = Founders(self.text)
        self.capital = Capital(self.text)
        self.inn = self.get_inn(self.text)
        self.kpp = self.get_kpp(self.text)
        self.filials = Filials(self.text)
        self.status = self.get_status(self.text)
        self.egrul_changes = self.get_okveds(
                                             self.text,
                                             'Сведения о документах, представленных при внесении записи в ЕГРЮЛ',
                                             EgrulChanges
                                             )


    def get_status(self, text):
        res = re.search(r'Сведения о прекращении юридического лица', text)
        if res:
            return 'организация является НЕ ДЕЙСТВУЮЩЕЙ!'
        else:
            return 'организация является действующей!'

    def get_okveds(self, text, pattern, clas):
        lst = []
        text = text.split(pattern)
        text = text[1:]
        if clas == Okveds:
            ind = re.search('Сведения о записях, внесенных в Единый государственный реестр юридических лиц', text[-1])
            if ind:
                ind1 = ind.span()[0]
                text[-1] = text[-1][:ind1]
        if clas == EgrulChanges:
            text = text[:-1]
        for item in text:
            okv = clas(item)
            lst.append(okv)
        return lst

    def get_reg_date(self, text):
        res = re.search(r'Дата регистрации\n(.*)', text)
        if res:
            return res.group(1)
        else:
            res = re.search(r'Дата регистрации до 1 июля 2002 года\n(.*)', text)
            if res:
                return res.group(1)
            else:
                return 'не найдено'

    def get_kpp(self, text):
        res = re.search(r'КПП юридического лица\n(.*)', text).group(1)
        return res

    def get_inn(self, text):
        res = re.search(r'ИНН юридического лица\n(.*)', text).group(1)
        return res

    def grn_reg_date(self, text):
        res = re.search(r'ГРН и дата внесения в ЕГРЮЛ записи,\nсодержащей указанные сведения\n(.*)\n(.*)', text)
        if not res:
            res = re.search(r'ГРН и дата внесения записи в ЕГРЮЛ\n(.*)\n(.*)', text)
        return res.group(1), res.group(2)
            

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
        self.index, self.city, self.street, self.building, *self.appartment = self.address
        self.grn, self.reg_date = EgrulData.grn_reg_date(self, self.text)
        self.city = make_capitalize(self.city)
        self.street = make_capitalize(self.street)

class Chefs(EgrulData):
    def __init__(self, text):
        self._begin_text = get_text(r'Сведения о лице, имеющем право без доверенности действовать от имени юридического\nлица', text)
        mark_end = re.search(r'Сведения об участниках /', text)
        self._text = self._begin_text[:mark_end.span()[0]]
        self.person = Person(self._text)
        self.post = Post(self._text)

class Post(Chefs):
    def __init__(self, text):
        self.text = get_text(r'Должность\n(.*)', text)
        self.post_name = re.search(r'Должность\n(.*)', text).group(1)
        self.grn, self.reg_date = EgrulData.grn_reg_date(self, self.text)

class Founders(EgrulData):
    def __init__(self, text):
        self._begin_text = get_text(r'Сведения об участниках / учредителях юридического лица', text)
        mark_end = re.search(r'Сведения об учете в налоговом органе', text)
        self._text = self._begin_text[:mark_end.span()[0]]
        self.persons = self.make_persons(self._text)
    
    def make_persons(self, text):
        prs = []
        pers = re.finditer(r'Фамилия\nИмя\nОтчество\n', text)
        points = list(map(lambda x: x.span()[0], pers))
        points.pop(0)
        for item in points:
            res = text[:item]
            person = Person(res)
            text = text[item:]
            prs.append(person)
        return prs
        
class Person(Chefs, Founders):
    def __init__(self, text):
        self._person = re.search(r'Фамилия\nИмя\nОтчество\n(.*\n){3}', text).group(0).split('\n')
        self._person = self._person[3:-1]
        self.surname, self.name, self.paternal = self._person
        self.inn = re.search(r'ИНН\n(.*)', text).group(1)
        self.grn, self.reg_date = EgrulData.grn_reg_date(self, text)

class Capital(EgrulData):
    def __init__(self, text):
        self.text = get_text(r'Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде\n', text)
        self.type = re.search(r'Вид\n(.*)', self.text).group(1)
        self.amount = re.search(r'Размер \(в рублях\)\n(.*)', self.text).group(1)
        self.grn, self.reg_date = EgrulData.grn_reg_date(self, self.text)

class Filials(EgrulData):
    def __init__(self, text):
        self._text = get_text(r'Адрес места нахождения филиала на\nтерритории Российской Федерации\n(.*){5}', text)
        if self._text:
            self.filials = 'hay'
        else:
            self.filials = 'Данных о филиалах организации не имеется.'

class Okveds(EgrulData):
    def __init__(self, text):
        self._text = text
        self.number = re.search(r'\n(.*)[А-Я]', self._text).group(1)
        self.number = self.number[:-1]
        self.name = self.get_name(self._text)
        self.grn, self.reg_date = EgrulData.grn_reg_date(self, self._text)

    def get_name(self, text):
        txt = clean_text(text)
        ind3 = re.search('[А-Я]', txt).span()[1]
        ind3 -= 1
        txt = txt[ind3:]
        txt = txt.split('\n')
        txt = ' '.join(txt)
        return txt

class EgrulChanges(EgrulData):
    def __init__(self, text):
        self._text = text
        self.document = clean_text(self._text)
        self.document = self.document.split('\n')
        self.document = ' '.join(self.document)
        self.grn, self.reg_date = EgrulData.grn_reg_date(self, self._text)

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
    text = text[0].lower()
    text = text[1].capitalize()
    return text

if '__name__' == '__main__':
    EgrulData()
