import datetime
import pdfr
import take_srn
import take_okfs
import take_bfo

class Company(pdfr.EgrulData, take_okfs.Okfs, take_bfo.Fo):
    
    def __init__(self):
        self.__init__ = pdfr.EgrulData.__init__(self)
        self.__init__ = take_okfs.Okfs.__init__(self)
        self.__init__ = take_bfo.Fo.__init__(self)
        self.srn = take_srn.main(str(self.inn))
        self.status = '---'
        self.company_staff = '---'
        self.common_info_text = input('Введите общую информацию о компании: ')
        self.telef = '---' 
        self.date = datetime.datetime.now().strftime("%d-%m-%Y")
        self.customer = input('Введите наименование заказчика: ') 
        self.gos_kontrakt = '---' 
        self.gos_zakupka = '---'
        self.current_text = self.get_current_text()
        self.egrul_changes = '---'
        self.important_facts = '---'
        self.factors = '---'
        self.ved = '---'

    def get_current_text(self):
        txt = '\n'
        txt += 'На {0} организация {1}.\n'.format(self.date, self.status.lower())
        txt += 'Среднесписочная численность работников организации - {0}\n'.format(self.company_staff.lower())
        txt += f'За {self.year}:\nприбыль - {self.income_this_year} рублей\nвыручка - {self.revenue_this_year} рублей\nсебестоимость продаж - {self.cost_of_sales_this_year} рублей\n'
        txt += f'Размер уставного капитала ({self.capital.type}) - {self.capital.amount} рублей,\nВыручка на начало 2020 года - {self.revenue_last_year} рублей\n'
        txt += f'Валовая прибыль на конец {self.year} - {self.gross_profit_this_year} рублей\n'
        txt += f'Общая сумма поступлений от текущих операций за 2020 год - {self.common_sum_this_year} рублей' 
        return txt
