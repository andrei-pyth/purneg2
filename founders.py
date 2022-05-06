import re
import file_orgzer as fo
from persons import Person

class Founders:
    def __init__(self, text):
        self._begin_text = fo.get_text(r'Сведения об участниках / учредителях юридического лица', text)
        self._mark_end = re.search(r'Сведения об учете в налоговом органе', self._begin_text)
        self._text = self._begin_text[:self._mark_end.span()[0]]
        self.persons = self.make_persons(self._text)
    
    def make_persons(self, text):
        prs = []
        pers = re.finditer(r'Фамилия\nИмя\nОтчество\n', text)
        list(map(lambda x: prs.append(Person(text[x.span()[0]:])), pers))
        return prs
