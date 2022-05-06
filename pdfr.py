import re
import get_egrul
import file_orgzer as fo
from okveds import Okveds
from egrul_changes import EgrulChanges
from capital import Capital
from location import Location
from founders import Founders
from chefs import Chefs
from filials import Filials
from facts import Facts
from lisences import Lisences #

class EgrulData:
    def __init__(self):
        get_egrul.main()
        fo.org_files('pdf_files', '.pdf', 'pdf_files/egrul.pdf', 'ЕГРЮЛ')
        self._text = fo.get_text_main('egrul')
        self.okveds = self.get_okveds(self._text)
        self.full_name = re.search(r'Настоящая выписка содержит сведения о юридическом лице\n(.*)', self._text).group(1)
        self.full_name_text = self.full_name.split('"')
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
        self.egrul_changes = self.get_egrul_changes(self._text)
        self.facts = '---'
        self.lisences = Lisences()

    def get_status(self, text):
        if re.search(r'Сведения о прекращении юридического лица', text):
            return 'ЮЛ является НЕ ДЕЙСТВУЮЩИМ!'
        else:
            return 'ЮЛ является действующим.'

    def get_egrul_changes(self, text):
        lst = []
        items = re.findall(r'ГРН и дата внесения записи в ЕГРЮЛ\n(.*)\n(.*)\n(\d+\n)?(Страница(.*)\n((.*)\n){10})?Причина внесения записи в ЕГРЮЛ\n(\D+\s)*\d+', text)
        for item in items:
            lst.append(EgrulChanges(item))
        return lst

    def get_okveds(self, text):
        lst = []
        items = re.findall(r'Код и наименование вида деятельности\n((\d+(\.)?)*)\s((\D+\s)*)(\d+\n)?(Страница(.*)\n((.*)\n){10})?ГРН и дата внесения в ЕГРЮЛ записи,\nсодержащей указанные сведения\n(.*)\n(.*)', text)
        for item in items:
            lst.append(Okveds(item))
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
