import uzip
import get_srn
import xml.etree.ElementTree as ET

def main(inn):
    get_srn.main() #Download archive from the web
    text = uzip.main() #Unzip the archive
    res = None
    while not res:
        try: res = parse_snr(next(text), inn)
        except StopIteration:
            break
    return res

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
