from selenium import webdriver

def auth(url):
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')
    options.add_argument('--enable-automation')
    options.add_argument('--remote-debugging-port=9230')
    options.add_argument('--enable-javascript')
    options.add_argument("--user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0'")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')
    options.add_experimental_option("prefs", {
      "download.default_directory": r"/home/chelnokov.a.a@kd-mid.lan/git/purneg/purneg2",
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "safebrowsing.enabled": True,
      "plugins.always_open_pdf_externally": True
    })
    browser = webdriver.Chrome(executable_path=r'/usr/bin/chromedriver', chrome_options=options)
    browser.get(url)
    return browser
