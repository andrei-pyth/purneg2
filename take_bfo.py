import pdfr
import file_orgzer
import get_bfo
import re

class Fo:
    def __init__(self):
        self._text = file_orgzer.get_text_main('bfo')
        self.year = re.search(r'Отчет о финансовых результатах\nЗа(.*)', self._text).group(1)
        print(self.year)
        self.income = re.search(r'налогообложения\n2300\n(.*)\n(.*)', self._text)
        self.income_this_year = self.income.group(1)
        print(self.income_this_year)
        self.income_last_year = self.income.group(2)
        self.revenue = re.search(r'Выручка4\n2110\n(.*)\n(.*)', self._text)
        self.revenue_this_year = self.revenue.group(1)
        self.revenue_last_year = self.revenue.group(2)
        self.cost_of_sales = re.search(r'продаж\n2120\n(.*)\n(.*)', self._text)
        self.cost_of_sales_this_year = self.cost_of_sales.group(1)
        self.cost_of_sales_last_year = self.cost_of_sales.group(2)
        self.gross_profit = re.search(r'Валовая прибыль \(убыток\)\n2100\n(.*)\n(.*)', self._text)
        self.gross_profit_this_year = self.gross_profit.group(1)
        print(self.gross_profit_this_year)
        self.gross_profit_last_year = self.gross_profit.group(2)
        self.common_sum = re.search(r'Поступления - всего\n4110\n(.*)\n(.*)', self._text)
        self.common_sum_this_year = self.common_sum.group(1)
        self.common_sum_last_year = self.common_sum.group(2)

def main():
    #get_bfo.main(inn)
    file_orgzer.org_files('pdf_files', '.pdf', 'pdf_files/bfo.pdf', 'БФО')
    res = Fo()
    return res
