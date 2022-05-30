import auth
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Accounts:
    
    def __init__(self, inn):
        self.inn = inn
        self.get_blocks()

    def get_blocks(self):
        browser = auth.auth('https://service.nalog.ru/bi.do')
        browser.execute_script("document.getElementById('unirad_0').click()")
        browser.execute_script(f"document.getElementById('innPRS').value='{self.inn}'")
        browser.execute_script("document.getElementById('bikPRS').value='044525225'")
        window = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="btnSearch"]'))
                )
        window.click()
        window = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/div/div[2]/div/div/div[2]/div[1]/button'))
                )
        window.click()
        sleep(3)
