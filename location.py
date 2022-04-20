import re
import file_orgzer as fo

class Location:
    def __init__(self, text):
        self._region_data = re.search(r'Место нахождения юридического лица\n(.*)\n(\d+\n)?(Страница(.*)\n((.*)\n){10})?ГРН и дата внесения в ЕГРЮЛ записи,\nсодержащей указанные сведения\n(.*)\n(.*)', text)
        self.region = self._region_data[1]
        self.region_grn = self._region_data[7]
        self.region_date = self._region_data[8]
        self._address = re.search(r'Адрес юридического лица\n((.*\n){1,15})', text)[1]
        self._lst = self._address.split('\n')
        self.index = self._lst.pop(0)
        self.city = self._lst.pop(0)
        self.reg_date = self._lst.pop(-4)
        self.grn = self._lst.pop(-4)
        self.address = self._lst[:-6]
