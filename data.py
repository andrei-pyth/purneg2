import datetime
import pdfr
import take_srn
import read_info_okfs

class Company(pdfr.EgrulData, read_info_okfs.Okfs):

    def __init__(self):
        self.__init__ = pdfr.EgrulData.__init__(self)
        self.__init__ = read_info_okfs.Okfs.__init__(self)
        self.srn = self.srn(str(self.inn))
        self.srn_for_text = self.srn_for_text(self.srn)
        self.status = '---'
        self.company_staff = '---'
        self.common_info_text = input('Введите общую информацию о компании: ')
        self.telef = '---' 
        self.date = datetime.datetime.now().strftime("%d-%m-%Y")
        self.customer = input('Введите наименование заказчика: ') 
        self.branches_lst = '---' 
        self.founders_text = '---'
        self.income = '---' 
        self.revenue = '---'
        self.cost_of_sales = '---'
        self.revenue_past = '---'
        self.gross_profit = '---'
        self.common_sum = '---'
        self.gos_kontrakt = '---' 
        self.gos_zakupka = '---'
        self.current_text = self.get_current_text()
        self.egrul_changes = '---'
        self.important_facts = '---'
        self.factors = '---'
        self.ved = '---'

    def srn_for_text(self, srn):
        if srn == 'ОСН':
            return 'ОСН\n(база данных ФНС на текущий момент сведений о наличии специальных режимов у контрагента не содержит)'
        else: return srn

    def srn(self, inn):
        res = take_srn.main(inn)
        if not res:
            return 'ОСН'
        else: return res

    def get_current_text(self):
        txt = '\n'
        txt += 'На {0} организация {1}.\n'.format(self.date, self.status.lower())
        txt += 'Среднесписочная численность работников организации - {0}\n'.format(self.company_staff.lower())
        txt += 'За 2020 год:\nприбыль - {0}\nвыручка - {1}\nсебестоимость продаж - {2}\n'.format(self.income, self.revenue, self.cost_of_sales)
        txt += 'Размер уставного капитала ({0}) - {1}\nВыручка на начало 2020 года - {2}\n'.format(self.capital.type, self.capital.amount, self.revenue_past)
        txt += 'Валовая прибыль на конец 2020 года - ' + self.gross_profit + '\n'
        txt += 'Общая сумма поступлений от текущих операций за 2020 год - {0}'.format(self.common_sum) 
        return txt
