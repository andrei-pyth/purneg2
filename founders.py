from persons import Person

class Founders:
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
