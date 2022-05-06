from auth import auth
from datetime import datetime as dt
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def main(inn):
    window = auth(f'https://zakupki.gov.ru/epz/organization/search/results.html?searchString={inn}&morphology=on')
    button1 = WebDriverWait(window, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                '/html/body/form/section[2]/div/div/div[1]/div[3]/div/div[1]/div[1]/div[1]/div[2]/div/a'
                ))
            )
    button1.click()
    input()
    button2 = WebDriverWait(window, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//*[@id="modal-region"]/div/div[4]/div/div[1]/div/button/span'
                ))
            )
    print(button2) 
    button2.click()  
    input()
