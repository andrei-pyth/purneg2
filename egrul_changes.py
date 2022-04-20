import file_orgzer as fo

class EgrulChanges:
    def __init__(self, text):
        self.grn = text[0]
        self.date = text[1]
        self.reason = fo.slt_jn(text[-1])
