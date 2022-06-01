import pdfr
import file_orgzer
import get_bfo
import re

class Fo:
    def __init__(self, inn):
        get_bfo.main(inn)
        file_orgzer.org_files('pdf_files', '.pdf', 'pdf_files/bfo.pdf', 'БФО')
        self._text = file_orgzer.get_text_main('bfo')
        self.income_pure_or_not = ''
        self.year = re.search(r'Код\nстроки\nНа 31 декабря\n(.*)', self._text).group(1)[:-5]
        self.income = re.search(r'\n2300\n(.*)\n(.*)', self._text)
        if self.income:
            self.income_this_year = self.income.group(1)
            self.income_last_year = self.income.group(2)
        else:
            self.income_pure = re.search(r'\(убыток\)\n2400\n(.*)\n(.*)', self._text)
            self.income_pure_this_year = self.income_pure.group(1)
            self.income_pure_last_year = self.income_pure.group(2)
            self.income_pure_or_not = '(чистая)'
        
        self.revenue = re.search(r'Выручка\d\n2110\n(.*)\n(.*)', self._text)
        self.revenue_this_year = self.revenue.group(1)
        self.revenue_last_year = self.revenue.group(2)

        self.cost_of_sales = re.search(r'продаж\n2120\n(.*)\n(.*)', self._text)
        if self.cost_of_sales:
            self.cost_of_sales_this_year = self.cost_of_sales.group(1)
            self.cost_of_sales_last_year = self.cost_of_sales.group(2)
        else:
            self.cost_of_sales_this_year = self.cost_of_sales_last_year = 'сведений не имеется'

        self.gross_profit = re.search(r'Валовая прибыль \(убыток\)\n2100\n(.*)\n(.*)', self._text)
        if self.gross_profit:
            self.gross_profit_this_year = self.gross_profit.group(1)
            self.gross_profit_last_year = self.gross_profit.group(2)
        else:
            self.gross_profit_this_year = self.gross_profit_last_year = 'сведений не имеется'

        self.common_sum = re.search(r'Поступления - всего\n4110\n(.*)\n(.*)', self._text)
        if self.common_sum:
            self.common_sum_this_year = self.common_sum.group(1)
            self.common_sum_last_year = self.common_sum.group(2)
        else:
            self.common_sum_this_year = self.common_sum_last_year = 'сведений не имеется'
        self.taxes = re.search(r'\n2410\n(.*)\(.*)', self._text)
        if self.taxes:
            self.taxes_this_year = self.taxes.group(1)
            self.taxes_last_year = self.taxes.group(2)
        else:
            self.taxes_this_year = self.taxes_last_year = 'Сведений не имеется'

def main(inn):
    return Fo(inn)
