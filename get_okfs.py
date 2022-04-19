from auth import auth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def main(inn):
    browser = auth('https://websbor.gks.ru/online/info')
    window = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="inn"]')))
    window.send_keys(inn)
    search_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
            '/html/body/websbor-root/div/div[1]/websbor-statistics-codes/websbor-simple-background/div/article/div/div[1]/div/form/div[3]/button'))
            )
    search_button.click()
    export_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/websbor-root/div/div[1]/websbor-statistics-codes/websbor-simple-background/div/article/div/div[2]/div/button'))
            )
    export_button.click()
    pdf_report_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/div/div/button[2]'))
            )
    pdf_report_button.click()
    sleep(2)
