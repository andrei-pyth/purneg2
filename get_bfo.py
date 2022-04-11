import auth
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main(inn):
    browser = auth.auth(f'https://bo.nalog.ru/search?query={inn}')
    button_overlay = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="short-info"]/div[2]/button'))
            )
    button_overlay.click()
    window = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div/div/div[2]/div[2]/a/div[1]/div[1]/div'))
            )
    window.click()
    download_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/button'))
            )
    download_button.click()
    sleep(20)
