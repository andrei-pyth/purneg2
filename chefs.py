import re
import file_orgzer as fo
from persons import Person

class Chefs:
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
