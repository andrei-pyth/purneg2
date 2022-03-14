import datetime
import pdfr
import company_keyb as ck
from bs4 import BeautifulSoup
from found import Founder
from direct import Direction
from egrul_ch import EgrulChanges

class Company():

    def __init__(self):
        self.ogrn = self.dct['ОГРН']
        self.inn = self.dct['ИНН']
        self.kpp = self.dct.get('КПП')
        self.okpo = self.dct['ОКПО']
        self.okopf = self.dct['ОКОПФ']
        self.okfs = self.dct['ОКФС']
        try: self.status = self.dct['Статус']
        except KeyError: self.status = 'Не указан'
        self.reg_data = self.dct['Дата первичной регистрации']
        self.company_full_name = self.dct['Полное наименование']
        self.company_short_name = self.dct['Сокращенное наименование']
        self.company_adress = self.dct['Адрес']
        try: self.company_staff = self.dct['Среднесписочная численность персонала:']
        except KeyError: self.company_staff = 'Не указана'
        self.common_info_text = input('Введите общую информацию о компании: ')
        try: self.nalog_regim = self.dct['Налоговый режим']
        except KeyError: self.nalog_regim = 'Не указан'
        self.form_sobst = self.dct['Форма собственности']
        self.org_pr_form = self.dct['Организационно-правовая форма']
        try: self.telef = self.dct['Телефон']
        except KeyError: self.telef = 'Не указан'
        self.date = datetime.datetime.now().strftime("%d-%m-%Y")
        self.customer = ck.Company.customer(self)
        try: self.ystav_kap = self.dct['Уставный капитал']
        except KeyError: self.ystav_kap = 'Не указан'
        self.branches_lst = self.find_branches()
        if self.branches_lst:
            self.branches_text = self.get_branches_text()
        else:
            self.branches_text = 'Организация не имеет филиалов'
        self.founders_text = self.founders_get()
        self.directors_text = self.get_director()
        self.income = self.get_income()
        self.revenue = self.get_revenue()
        self.cost_of_sales = self.get_cost_of_sales()
        self.revenue_past = self.get_revenue_past()
        self.gross_profit = self.get_gross_profit()
        self.common_sum = self.get_common_sum()
        self.ved = self.get_ved()
        self.gos_kontrakt = self.get_gos_kontrakt()
        self.gos_zakupka = self.get_gos_zakupka()
        self.current_text = self.get_current_text()
        self.egrul_changes = self.get_egrul_changes()
        self.important_facts = self.get_important_facts()
        self.factors = self.get_factors()
        self.activities_list = pdfr.main(self.ogrn)
        print(self.activities_list)
        self.activities_text = self.get_activities_text(self.activities_list)

    def get_activities_text(self, lst):
        txt = ''
        for item in lst:
            print(item)
            txt += item + '\n'
        return txt

    def get_factors(self):
        txt = ''
        res = self._soup.find('div', {'class':'bu_result_container Main_Card_CardUl_RiskFactors group_Main_Card_CardUl'})
        if res:
            res = res.find_all('p')
            count = 0
            for item in res:
                count += 1
                txt += '\n\t' + str(count) + ') ' + item.text + ';\n'
        else:
            txt = 'не имеется'
        return txt

    def get_important_facts(self):
        txt = ''
        res = self._soup.find_all('div', {'class':'page-content-company-vestnik return'})
        for item in res:
            text = item.find('strong').text
            txt += '\n\t' + text
        return txt

    def get_egrul_changes(self):
        txt = ''
        res =  self._soup.find('div', {'class':'bu_result_container Main_Important_ImportantUl_Egrul group_Main_Important_ImportantUl'})
        if res:
            res = res.find('tbody').find_all('tr')
            ln = len(res)
            if ln > 5:
                res = res[:5]
            for item in res:
                obj = EgrulChanges(item)
                if not obj.svidetelstvo:
                    obj.svidetelstvo = 'сведений не имеется'
                txt += '\n\tДата внесения записи: ' + obj.date.text + '\n\tГРН: ' + obj.grn.text + '\n\t' + obj.text_of_change.text + '\n\tРеквизиты свидетельства: ' + obj.svidetelstvo.text.strip() + '\n' 
            return txt
        else:
            return 'сведений об изменениях не имеется'

    def get_gos_zakupka(self):
        return '--'

    def get_gos_kontrakt(self):
        return '--'

    def get_ved(self):
        return 'Компания не является участником внешнеэкономической деятельности.'

    def get_common_sum(self):
        return '--'

    def get_gross_profit(self):
        return '--'

    def get_revenue_past(self):
        return '--'

    def get_cost_of_sales(self):
        return '--'

    def get_revenue(self):
        return '--'

    def get_income(self):
        res = self._soup.find_all('td', string='Чистая прибыль (убыток) отчётного периода')
        print(res)
        return res

    def get_current_text(self):
        txt = '\n'
        txt += '\tНа {0} организация {1}.\n'.format(self.date, self.status.lower())
        txt += '\tСреднесписочная численность работников организации - {0}\n'.format(self.company_staff.lower())
        txt += '\tЗа 2020 год:\n\tприбыль - {0}\n\tвыручка - {1}\n\tсебестоимость продаж - {2}\n'.format(self.income, self.revenue, self.cost_of_sales)
        txt += '\tРазмер уставного капитала (уставной фонд) - {0}\n\tВыручка на начало 2020 года - {1}\n'.format(self.ystav_kap, self.revenue_past)
        txt += '\tВаловая прибыль на конец 2020 года - ' + self.gross_profit + '\n'
        txt += '\tОбщая сумма поступлений от текущих операций за 2020 год - {0}'.format(self.common_sum) 
        return txt

    def get_director(self):
        res = self._soup.find('div', {'class':'bu_result_container Main_Card_CardUl_Controls_Egrul group_Main_Card_CardUl_Controls'})
        if res:
            res1 = res.find('tbody')
        else:
            return 'Сведения о руководителях не найдены'
        res2 = res1.find_all('tr')
        txt = ''
        for item in res2:
            director = Direction(item)
            txt += '{0}) {2} - {1}\n    начиная c {3}'.format(director.number, director.name,\
                    director.post, director.date)
        return txt

    def founders_get(self):
        txt = ''
        res = self._soup.find('div', {'class':'bu_result_container Main_Card_CardUl_Founders_Egrul group_Main_Card_CardUl_Founders'})
        if res:
            res1 = res.find('tbody')
        else:
            return 'сведений об учредителях не имеется'
        res2 = res1.find_all('tr')
        for item in res2:
            founder = Founder(item)
            txt += '\n{0}) {1}\n    {2} рублей\n    {3} % уставного капитала\n    дата регистрации {4}\n'.format(founder.number, founder.name,\
                    founder.rub_capital, founder.percent_capital, founder.date)
        return txt

    def get_soup(self):
        fle = input('Введите название файла: ')
        with open(fle, 'r', encoding='Windows-1251') as f:
            contents = ''
            while True:
                try:
                    line = f.readline()
                    if line:
                        contents += line
                    else:
                        print('Vse!!!')
                        return BeautifulSoup(contents, 'lxml')
                except UnicodeDecodeError as err:
                    print(err)
                    continue


    def find_branches(self):
        res = self._soup.find('div', {'class':'bu_result_container Main_Card_CardUl_Branch_Egrul group_Main_Card_CardUl_Branch'})
        if res:
            res1 = res.find_all('tr')
        else:
            return 
        lst = []
        if len(res1) > 10:
            choice = input('Найдено {} филиалов.\n1) Включить в справку все филиалы \n2) Включить только первые 10 \n'.format(len(res1)))
            if choice == '1':
                res2 = res1
            elif choice == '2':
                res2 = res1[:10]
            for item in res2[1:]:
                lst2 = []
                data = item.find_all('td')
                for it in data:
                    lst2.append(it.text.strip())
                lst.append(lst2)
        return lst

    def get_branches_text(self):
        res = ''
        for item in self.branches_lst:
            res += '\n'
            res += item[0] + ') ' + item[1] + '\n ' + item[2] + '\n ' + item[3] + '\n ОГРН: ' + item[4] + '\n'
        return res

    def find_table(self):
        return self._soup.find('table', {'class':'print-main-info'})

    def find_data(self):
        return self._table.find_all('tr')

    def make_dct(self):
        dct = {} 
        for item in self._data:
            res = item.find_all('td')
            dct[res[0].text] = res[1].text
        print(dct)
        return dct
