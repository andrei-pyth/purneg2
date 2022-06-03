import re

class Capital:
    def __init__(self, text):
        self._type = re.search(r'/ паевом фонде\n\d+\nВид\n(.*)', text)
        self.type = self._type.group(1)
        self._amount = re.search(r'Размер \(в рублях\)\n(.*)', text)
        self.amount = self._amount[1]
        self._grn = self._amount.span(1)[1]
        self._text = text[self._grn:]
        self._grndt = re.search(r'ГРН и дата внесения в ЕГРЮЛ записи,\nсодержащей указанные сведения\n(.*)\n(.*)', self._text)
        self.grn = self._grndt.group(1)
        self.date = self._grndt.group(2)
