import auth
from time import sleep
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main(inn):
    browser = auth.auth('https://service.nalog.ru/bi.do')
    browser.execute_script("document.getElementById('unirad_0').click()")
    browser.execute_script(f"document.getElementById('innPRS').value='{inn}'")
    browser.execute_script("document.getElementById('bikPRS').value='044525225'")
    window = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="btnSearch"]'))
            )
    window.click()
    try:
        window = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/div/div[2]/div/div/div[2]/div[1]/button'))
                )
    except TimeoutException:
        window = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/div/div[2]/div/div/ul/div[7]/div[1]/button'))
                )
    window.click()
    sleep(5)
