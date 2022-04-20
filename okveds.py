import file_orgzer as fo

class Okveds:
    def __init__(self, text):
        self.number = text[0] 
        self.name = fo.slt_jn(text[3])
        self.grn = text[-2]
        self.reg_date = text[-1]
