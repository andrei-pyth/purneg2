

class Facts:
    def __init__(self):
        self.fact_capital = self.get_cap_fact()

    def get_cap_fact(self):
        if int(self.capital.amount) <= 10000:
            return 'Размер уставного капитала составляет минимальную сумму 10000 или меньше;'
