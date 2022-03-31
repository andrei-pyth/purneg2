import uzip.py
import xml.etree.ElementTree as ET

def main(inn):
    text = uzip.main()
    string = next(text)
    root = ET.fromstring(string)
    fn = lambda x: root[x][0].attrib['ИННЮЛ']


