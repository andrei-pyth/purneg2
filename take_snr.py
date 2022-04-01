import uzip
import get_srn
import xml.etree.ElementTree as ET

def main(inn):
    get_srn.main() #Download archive from the web
    text = uzip.main() #Unzip the archive
    res = None
    while not res:
        res = parse_snr(next(text))
    return res

def parse_snr(string):
    root = ET.fromstring(string)
    range_fin = len(root)
    fn = lambda x: root[x][0].attrib['ИННЮЛ']
    for it in range(1, range_fin):
        if inn == fn(it):
            dic = root[it][1].attrib
            for key, value in dic.items():
                if value == '1':
                    return key[5:]
    return
