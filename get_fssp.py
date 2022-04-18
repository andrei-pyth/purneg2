import requests
from datetime import datetime

def get_file():
    day = datetime.today().day
    return requests.get(f'http://opendata.fssp.gov.ru/7709576929-iplegallist/data-202204{day}-structure-20200401.csv', stream=True)
    
def get_case(csv):
    lst = []
    while True:
        res = csv.raw.read(1)
        if res == b'\n':
            res1 = b''.join(lst)
            lst.clear()
            yield res1.decode('utf-8')
        else:
            lst.append(res)

def check(text):
    if 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "СФЕРА"' in text:
        print('Нашлось!!!!')
        return text
    else: 
        return
    
def main():
    fl = get_file()
    res = get_case(fl)
    count = 0
    res1 = check(next(res))
    while not res1:
        count += 1
        res1 = check(next(res))
        print(count)
        if count%10 == 0:
            print(res1)

if '__name__' == '__main__':
    main()

    

