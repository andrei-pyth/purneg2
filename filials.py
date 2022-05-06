import file_orgzer as fo

class Filials:
    def __init__(self, text):
        self._text = fo.get_text(r'Адрес места нахождения филиала на\nтерритории Российской Федерации\n(.*){5}', text)
        if self._text:
            self.filials = 'hay'
        else:
            self.filials = 'Данных о филиалах организации не имеется.'
