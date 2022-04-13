from auth import auth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def main(full_name):
    browser = auth('https://opendata.fssp.gov.ru/opendataform/action/opendata')

