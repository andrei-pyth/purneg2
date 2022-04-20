import re

class Capital:
    def __init__(self, text):
        self.type = re.search(r'/ паевом фонде\n\d+\nВид\n(.*)', text)
        self._data = re.search(r'Размер \(в рублях\)\n(.*)\n(\d+\n)?(Страница(.*)\n((.*)\n){10})?ГРН и дата внесения в ЕГРЮЛ записи,\nсодержащей указанные сведения\n(.*)\n(.*)', text)
        self.amount = self._data[1]
        self.grn = self._data[7]
        self.date = self._data[8]
