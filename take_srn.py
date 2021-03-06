import uzip
import get_srn
import xml.etree.ElementTree as ET
from time import sleep

def main(inn, url, name):
    get_srn.main(url, name) #Download archive from the web
    sleep(1)
    text = uzip.main('srn.zip') #Unzip the archive
    if text:
        res = None
        while not res:
            try: 
                res = parse_snr(next(text), inn)
                if res:
                    return res
            except StopIteration:
                return 'ОСН\n(база данных ФНС на текущий момент сведений о наличии специальных режимов налогообложения у контрагента не содержит)'
    else:
        print('Файл не загрузился или загрузился с ошибкой. Попробуем ещё раз.')
        main(inn, url, name)


def parse_snr(string, inn):
    root = ET.fromstring(string)
    range_fin = len(root)
    fn = lambda x: root[x][0].attrib['ИННЮЛ']
    for it in range(1, range_fin):
        if inn == fn(it):
            dic = root[it][1].attrib
            for key, value in dic.items():
                if value == '1':
                    print('Данные об СРН найдены в базе данных ФНС')
                    return key[5:]
    return
