import wget
import file_orgzer
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auth import auth
from time import sleep

def get_srn(url, name):
    browser = auth(url)
    window = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,
                '/html/body/form/div[3]/div[1]/div[4]/div[2]/div/div/div/div[2]/div[2]/table/tbody/tr[9]/td[3]/a')))
    if window:
        lnk = window.get_attribute('href')
        print(f'Ссылка на базу данных {name} найдена!!!  ===>  {lnk}')
        browser.quit()
        try:
            wget.download(lnk)
            sleep(2)
        except urllib.error.HTTPError:
            print(f'Загрузка базы {name} не удалась. Попробуем снова.')
            get_srn(url, name)
    else:
        print(f'Ссылка на базу данных {name} НЕ найдена!!!')

def main(url, name):
    get_srn(url, name)
    if name == 'СРН':
        file_name = 'srn.zip'
    elif name == 'ССЧС':
        file_name = 'schs.zip'
    file_orgzer.org_files('zip_files', '.zip', f'zip_files/{file_name}', name) 
