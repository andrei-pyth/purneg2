import re
import file_orgzer as fo

class Person:
    def __init__(self, text):
        self._person = re.search(r'Фамилия\nИмя\nОтчество\n(.*\n){3}', text).group(0).split('\n')
        self._person = self._person[3:-1]
        self.surname, self.name, self.paternal = self._person
        self.inn = re.search(r'ИНН\n(.*)', text).group(1)
        self.grn, self.reg_date = fo.grn_reg_date(text)
