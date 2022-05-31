import datetime
import pdfr
import take_srn
import take_okfs
import take_bfo
import take_schs
import taxes #
import take_blocks 
import reliability #
#import get_gos_kont

class Company(pdfr.EgrulData, take_okfs.Okfs, take_bfo.Fo):
    
    def __init__(self):
        self.__init__ = pdfr.EgrulData.__init__(self)
        self.__init__ = take_okfs.Okfs.__init__(self, self.inn)
        self.__init__ = take_bfo.Fo.__init__(self, self.inn)
        self.srn = take_srn.main(
                self.inn, 
                'https://data.nalog.ru/opendata/7707329152-snr/',
                'СРН'
                )
        self.schs = take_schs.main(
                self.inn,
                'https://www.nalog.gov.ru/rn32/opendata/7707329152-sshr2019/',
                'ССЧС'
                )
        self.accounts_blocked = take_blocks.main(self.inn)
        if not self.income:
            self.income_this_year = self.income_pure_this_year
            self.income_last_year = self.income_pure_last_year
        self.common_info_text = input('Введите общую информацию о компании: ')
        self.telef = '---' 
        self.date = datetime.datetime.now().strftime("%d-%m-%Y")
        self.customer = self.get_customer()
        self.gos_kontrakt = '---' 
        self.gos_zakupka = '---'
        self.current_text = self.get_current_text()
        self.factors = '---'
        self.ved = '---'
        self.facts = '---'
        self.important_facts = '---'
        self.taxes = taxes.Taxes()
        self.reliability = reliability.Reliability()
        self.applications = '---'

    def get_customer(self):
        first = 'ПАО Калужская сбытовая компания'
        second = 'АО Калужская городская энергетическая компания'
        ch = int(input(f'Введите номер заказчика:\n1) {first}\n2) {second}\n\n '))
        if ch == 1:
            return first
        elif ch == 2:
            return second
        else:
            print('Введите номер правильно!')
            self.get_customer()


    def get_current_text(self):
        txt = '\n'
        txt += 'На {0} {1}\n\n'.format(self.date, self.status)
        txt += 'Среднесписочная численность работников организации - {0}\n\n\n'.format(self.schs)

        txt += f'За {self.year} год:\n\nприбыль{self.income_pure_or_not} - {self.income_this_year} рублей\n\nвыручка - {self.revenue_this_year} рублей\n\nсебестоимость продаж - {self.cost_of_sales_this_year} рублей\n\n\n'
        txt += f'Размер уставного капитала ({self.capital.type}) - {self.capital.amount} рублей,\n\n\nВыручка на начало 2020 года - {self.revenue_last_year} рублей\n\n\n'
        txt += f'Валовая прибыль на конец {self.year} - {self.gross_profit_this_year} рублей\n\n\n'
        txt += f'Общая сумма поступлений от текущих операций за 2020 год - {self.common_sum_this_year} рублей' 
        return txt
