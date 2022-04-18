import re
import get_egrul
import file_orgzer as fo


class EgrulData:
    def __init__(self):
        get_egrul.main()
        fo.org_files('pdf_files', '.pdf', 'pdf_files/egrul.pdf', 'ЕГРЮЛ')
        self._text = fo.get_text_main('egrul')
        self.okveds = self.get_okveds(
                                      self._text,
                                      'Код и наименование вида деятельности',
                                      Okveds
                                      )
        self.full_name = re.search(r'Настоящая выписка содержит сведения о юридическом лице\n(.*)', self._text).group(1)
        self.ogrn = re.search(r'ОГРН(.*)', self._text).group(1)
        self.ogrn = self.ogrn.split()
        self.ogrn = ''.join(self.ogrn)
        self.name_grn = fo.grn_reg_date(self._text)[0]
        self.name_reg_date = fo.grn_reg_date(self._text)[1]
        self.short_name = re.search(r'Сокращенное наименование на русском\nязыке\n(.*)', self._text).group(1)
        self.location_adress = Location(self._text)
        self.creation_method = re.search(r'Способ образования\n(.*)', self._text).group(1)
        self.reg_date = self.get_reg_date(self._text)
        self.chefs = Chefs(self._text)
        self.founders = Founders(self._text)
        self.capital = Capital(self._text)
        self.inn = re.search(r'ИНН юридического лица\n(.*)', self._text).group(1)
        self.kpp = re.search(r'КПП юридического лица\n(.*)', self._text).group(1)
        self.filials = Filials(self._text)
        self.status = self.get_status(self._text)
        self.egrul_changes = self.get_okveds(
                                             self._text,
                                             'Сведения о документах, представленных при внесении записи в ЕГРЮЛ',
                                             EgrulChanges
                                             )
        self.facts = '---'

    def get_status(self, text):
        res = re.search(r'Сведения о прекращении юридического лица', text)
        if res:
            return 'ЮЛ является НЕ ДЕЙСТВУЮЩИМ!'
        else:
            return 'ЮЛ является действующим.'

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

class Location(EgrulData):
    def __init__(self, text):
        self.text = fo.get_text(r'Место нахождения и адрес юридического лица\n', text)
        self.region = LocationRegion(self.text)
        self.address = LocationAddress(self.text)

class LocationRegion(Location):
    def __init__(self, text):
        self.region_name = re.search(r'Место нахождения юридического лица\n(.*)', text).group(1)
        self.grn, self.reg_date = fo.grn_reg_date(text)

class LocationAddress(Location):
    def __init__(self, text):
        self._text = fo.get_text(r'Адрес юридического лица\n', text)
        self._address = re.search(r'Адрес юридического лица\n(.*\n){5}', text).group(0).split('\n')
        self.address = self._address[1:-1]
        self.index, self.city, self.street, self.building, *self.appartment = self.address
        self.grn, self.reg_date = fo.grn_reg_date(self._text)
        self.city = fo.make_capitalize(self.city)
        self.street = fo.make_capitalize(self.street)

class Chefs(EgrulData):
    def __init__(self, text):
        self._begin_text = fo.get_text(r'Сведения о лице, имеющем право без доверенности действовать от имени юридического\nлица', text)
        mark_end = re.search(r'Сведения об участниках /', text)
        self._text = self._begin_text[:mark_end.span()[0]]
        self.person = Person(self._text)
        self.post = Post(self._text)

class Post(Chefs):
    def __init__(self, text):
        self._text = fo.get_text(r'Должность\n(.*)', text)
        self.post_name = re.search(r'Должность\n(.*)', text).group(1)
        self.grn, self.reg_date = fo.grn_reg_date(self._text)

class Founders(EgrulData):
    def __init__(self, text):
        self._begin_text = fo.get_text(r'Сведения об участниках / учредителях юридического лица', text)
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
        self.grn, self.reg_date = fo.grn_reg_date(text)

class Capital(EgrulData):
    def __init__(self, text):
        self._text = fo.get_text(r'Сведения об уставном капитале / складочном капитале / уставном фонде / паевом фонде\n', text)
        self.type = re.search(r'Вид\n(.*)', self._text).group(1)
        self.amount = re.search(r'Размер \(в рублях\)\n(.*)', self._text).group(1)
        self.grn, self.reg_date = fo.grn_reg_date(self._text)

class Filials(EgrulData):
    def __init__(self, text):
        self._text = fo.get_text(r'Адрес места нахождения филиала на\nтерритории Российской Федерации\n(.*){5}', text)
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
        self.grn, self.reg_date = fo.grn_reg_date(self._text)

    def get_name(self, text):
        txt = fo.clean_text(text)
        ind3 = re.search('[А-Я]', txt).span()[1]
        ind3 -= 1
        txt = txt[ind3:]
        txt = fo.slt_jn(txt)
        return txt

class EgrulChanges(EgrulData):
    def __init__(self, text):
        self._text = text
        self._document = fo.clean_text(self._text)
        self.document = fo.slt_jn(self._document) 
        self._reason = re.search(r'Причина внесения записи в ЕГРЮЛ\n(.*\n)\d+', self._text)
        if self._reason:
            self.reason = fo.slt_jn(self._reason.group(1))
        else:
            print('Причина внесения изменений в ЕГРЮЛ не получена')
            self.reason = '---'
        self.grn, self.reg_date = fo.grn_reg_date(self._text)

class Facts(EgrulData):
    def __init__(self):
        self.fact_capital = self.get_cap_fact()

    def get_cap_fact(self):
        if int(self.capital.amount) <= 10000:
            return 'Размер уставного капитала составляет минимальную сумму 10000 или меньше;'
