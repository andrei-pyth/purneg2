from auth import auth
from selenium.webdriver.common.by import By
from time import sleep

def main(inn):
    browser = auth('https://websbor.gks.ru/online/info')
    window = browser.find_element(by=By.XPATH, value='//*[@id="inn"]')
    window.send_keys(inn)
    sleep(2)
    search_button = browser.find_element(by=By.XPATH, value='/html/body/websbor-root/div/div[1]/websbor-statistics-codes/websbor-simple-background/div/article/div/div[1]/div/form/div[3]/button')
    search_button.click()
    sleep(2)
    export_button = browser.find_element(by=By.XPATH, value='/html/body/websbor-root/div/div[1]/websbor-statistics-codes/websbor-simple-background/div/article/div/div[2]/div/button')
    export_button.click()
    sleep(2)
    pdf_report_button = browser.find_element(by=By.XPATH, value='/html/body/div[3]/div[2]/div/div/div/button[2]')
    pdf_report_button.click()
    sleep(2)
    export_button = browser.find_element(by=By.XPATH, value='/html/body/websbor-root/div/div[1]/websbor-statistics-codes/websbor-simple-background/div/article/div/div[2]/div/button')
    export_button.click()
