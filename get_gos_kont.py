from auth import auth
from datetime import datetime as dt
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class GosZakup():
    def __init__(self, inn):
        self._browser = get_browser(inn)
        self.quantity = get_quantity()

def get_browser(inn):
    date_start = dt.today() - dt.timedelta(days=1095)
    date_finish = dt.today()
    browser = auth(f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={inn}&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&currencyIdGeneral=-1&publishDateFrom={date_start:%d.%m.%Y}&publishDateTo={date_finish:%d.%m.%Y}')
    return browser

def get_quantity(browser):
    quantity = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((
                                            By.XPATH,
                                            '/html/body/form/section[2]/div/div/div[1]/div[1]/div[2]'
                                            ))
    return quantity

def report_download(browser):
    window = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((
                                            By.XPATH,
                                            '/html/body/form/section[2]/div/div/div[1]/div[2]/div[1]/div[2]/a[1]'
                                            ))
    window.click()
    dld_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((
                                            By.XPATH,
                                            '/html/body/div[3]/div/div/div[3]/div[4]/div[2]/div/div[1]/div[1]/div/div[2]'
                                            ))
    dld_button.click()

