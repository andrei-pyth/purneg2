import get_okfs
import re
import file_orgzer
from file_orgzer import get_text

class Okfs:

    def __init__(self):
        self._text = file_orgzer.get_text_main('okfs')
        self._text = get_text(r'Расшифровка кодов ОК ТЭИ', self._text)
        self.okpo = re.search(r'ОКПО\):\n(\d+)', self._text).group(1)
        self.okato = re.search(r'ОКАТО\):\n(\d+)\s\((\w+)', self._text).group(1)
        self.okato_text = re.search(r'ОКАТО\):\n(\d+)\s\((.*)\)', self._text).group(2)
        self.oktmo = re.search(r'ОКТМО\):\n(\d+)', self._text).group(1)
        self.oktmo_text = re.search(r'ОКТМО\):\n(\d+)\s\((.*)\)', self._text).group(2)
        self.okogy = re.search(r'ОКОГУ\):\n(\d+)', self._text).group(1)
        self.okogy_text = re.search(r'ОКОГУ\):\n(\d+)\s\((.*[\n]?.*)\)', self._text).group(2)
        self.okfs = re.search(r'ОКФС\):\n(\d+)', self._text).group(1)
        self.okfs_text = re.search(r'ОКФС\):\n(\d+)\s\((.*)\)', self._text).group(2)
        self.okopf = re.search(r'ОКОПФ\):\n(\d+)', self._text).group(1)
        self.okopf_text = re.search(r'ОКОПФ\):\n(\d+)\s\((.*)\)', self._text).group(2)
         
def main(inn):
    get_okfs.main()
    file_orgzer.org_files('pdf_files', '.pdf', 'pdf_files/okfs.pdf', 'ОКФС')
    res = Okfs()
    return res
