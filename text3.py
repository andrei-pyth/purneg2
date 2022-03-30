import data as cr
from docx import Document
from docx.shared import Cm
from docx.shared import Pt
from docx.shared import RGBColor

class DocText():

    def __init__(self, comp):
        self.document = Document()
        self.comp = comp

        section = self.document.sections[0]
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(3)
        section.right_margin = Cm(1)
        
        
        self.style = self.document.styles['Normal']
        self.font = self.style.font
        self.font.name = 'Time New Roman'
        self.font.size = Pt(14)
        self.font.bold = False

        self.style2 = self.document.styles['Heading 1']
        self.style2.next_paragraph_style = self.document.styles['Normal']
        self.font2 = self.style2.font
        self.font2.color.rgb = RGBColor(80, 80, 80)
        self.font2.name = 'Arial'
        self.font2.size = Pt(18)
        self.font2.italic = True
        self.font2.bold = False
        
        self.front_page()
        self.common_info()

    def front_page(self):
        self.paragraph = self.document.add_paragraph('Результаты проверки компании \n\n\n\n\n')
        self.paragraph.style = self.document.styles['Heading 1']
        self.paragraph.alignment = 1

        self.sentence = self.paragraph.add_run(self.comp.company_full_name + '\n\n\n\n\n')
        self.sentence.font.bold = True
        self.sentence.font.size = Pt(20)

        self.sentence = self.paragraph.add_run('на предмет соответствия требованиям к контрагентам\n')
        self.sentence.font.bold = False

        self.sentence = self.paragraph.add_run('"' + self.comp.customer + '"\n\n\n\n\n\n')
        self.sentence.font.bold = True

        self.sentence = self.paragraph.add_run(self.comp.date)
        self.sentence.font.bold = False

        self.sentence = self.paragraph.add_run('\nг.Санкт-Петербург')

        self.document.add_page_break()

    def common_info(self):

        self.document.add_paragraph('Общая информация:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.common_info_text + '\n').alignment = 3
        
        self.document.add_paragraph('Полное наименование компании:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.full_name + '\n')

        self.document.add_paragraph('Краткое наименование компании:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.short_name + '\n')
                
        self.document.add_paragraph('Налоговый режим:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.nalog_regim + '\n')
        
        self.document.add_paragraph('Форма собственности:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.form_sobst + '\n')
        
        self.document.add_paragraph('Организационно-правовая форма:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.org_pr_form + '\n')

        self.document.add_paragraph('При регистрации организации присвоены:\n').style = self.document.styles['Heading 1']
        table = self.document.add_table(rows=6, cols=2)
        table.cell(0, 0).text = 'ОГРН'
        table.cell(0, 1).text = self.comp.ogrn
        table.cell(1, 0).text = 'ИНН'
        table.cell(1, 1).text = self.comp.inn
        table.cell(2, 0).text = 'КПП'
        if self.comp.kpp:
            table.cell(2, 1).text = self.comp.kpp
        else:
            table.cell(2, 1).text = ''
        table.cell(3, 0).text = 'ОКПО'
        table.cell(3, 1).text = self.comp.okpo
        table.cell(4, 0).text = 'ОКФС'
        table.cell(4, 1).text = self.comp.okfs
        table.cell(5, 0).text = 'ОКОПФ'
        table.cell(5, 1).text = self.comp.okopf
        
        self.document.add_paragraph('Статус:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.status + '\n')

        self.document.add_paragraph('Дата первичной регистрации:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.reg_data + '\n')

        self.document.add_paragraph('Размер уставного капитала:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.ystav_kap + '\n')

        self.document.add_page_break()

        self.document.add_paragraph('Юридический адрес компании:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.company_adress + '\n')
        
        self.document.add_paragraph('Официальный сайт и интернет-ресурсы компании:\n\n').style = self.document.styles['Heading 1']

        self.document.add_paragraph('Филиалы и представительства:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.branches_text + '\n')
        
        self.document.add_paragraph('Учредители компании:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.founders_text + '\n')
        
        self.document.add_paragraph('Руководители компании:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.directors_text + '\n')

        self.document.add_paragraph('Последние изменения в ЕГРЮЛ:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.egrul_changes + '\n')
        
        self.document.add_paragraph('Опубликованные юридически значимые факты:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.important_facts + '\n')
        
        self.document.add_paragraph('Данные о текущей деятельности:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.current_text + '\n')

        self.document.add_paragraph('Данные о внешнеэкономической деятельности:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.ved + '\n')

        self.document.add_paragraph('Участие в государственных закупках или госконтрактах:').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.gos_zakupka + '\n' + self.comp.gos_kontrakt + '\n')

        self.document.add_page_break()
        
        self.document.add_paragraph('Иные значимые факторы: ').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.factors + '\n')
        
        self.document.add_page_break()
        
        self.document.add_paragraph('Виды деятельности: ').style = self.document.styles['Heading 1']
        self.document.add_paragraph('\n\t' + self.comp.activities_text + '\n')
        


def save_doc(doc):
    fl = input('Введите название файла с результатом: ')
    doc.save(fl)

def main():
    comp = cr.Company()
    doc = DocText(comp)
    save_doc(doc.document)

if __name__ == '__main__':
    main()
      