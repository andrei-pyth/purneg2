import wget
import file_orgzer
from selenium.webdriver.common.by import By
from auth import auth
from time import sleep

def get_srn():
    browser = auth('https://data.nalog.ru/opendata/7707329152-snr/')
    sleep(2)
    window = browser.find_element(by=By.XPATH, value='/html/body/form/div[3]/div[1]/div[4]/div[2]/div/div/div/div[2]/div[2]/table/tbody/tr[9]/td[3]/a')
    if window:
        lnk = window.get_attribute('href')
        print(f'Ссылка на базу данных найдена!!!  ===>  {lnk}')
        r = wget.download('https://data.nalog.ru/opendata/7707329152-snr/data-20220117-structure-20180801.zip')
        #window.click()
    else:
        print('Ссылка на базу данных НЕ найдена!!!')

def main():
    get_srn()
    file_orgzer.check_download('.zip')
    file_orgzer.org_files('zip_files', '.zip', 'zip_files/srn.zip', 'СНР') 
