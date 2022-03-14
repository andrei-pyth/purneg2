from time import sleep
from auth import auth

class SerRes():
    pass

def main():
    inn = input('INN ')
    browser = auth('http://egrul.nalog.ru/')
    window = browser.find_element_by_xpath('//*[@id="query"]')
    window.send_keys(inn)
    window2 = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div/form/div/div[1]/div[4]/div/div[1]/div/ul/li')
    window2.click()
    browser.switch_to.frame('uniDialogFrame')
    sleep(2)
    button = browser.find_element_by_xpath('//*[@id="btn_toggle"]')
    button.click()
    button2 = browser.find_element_by_xpath('//*[@id="btn_ok"]')
    button2.click()
    browser.switch_to.default_content()
    browser.find_element_by_xpath('//*[@id="btnSearch"]').click()
    sleep(2)
    res = get_search_res(browser)
    if not res:
        print('По заданным параметрам в базе ЕГРЮЛ ничего не найдено')
        browser.quit()
    else:
        show_rs2_res(res)
        browser.quit()
        print('Выписка из ЕГРЮЛ скачана!')
        
def get_search_res(browser):
    title = browser.find_elements_by_xpath('//*[@id="resultContent"]/div/div[2]/a')
    text = browser.find_elements_by_class_name('res-text')
    buttons = browser.find_elements_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div[4]/div/div[3]/button')
    return title, text, buttons

def show_rs2_res(res):
    display_objs = make_objs(res[0], res[1], res[2])
    if len(display_objs) > 10:
        print('Найдено слишком много организаций. Уточните параметры поиска, указав ИНН или ОГРН.')
    elif not display_objs:
        print('По Вашему запросу ничего не найдено.')
    else:
        make_choice(display_objs)

def make_choice(objs):
    for item in objs:
        print('{}) {};\n'.format(item.count, item.text)) 
    res = input('Введите номер интересующей Вас организации: ')
    objs[int(res)-1].button.click()
    sleep(2)
    print('Выписка или выписки из ЕГРЮЛ скачаны.')
    if not res.isdigit() or int(res) > len(objs):
        print('Уточните параметры ввода')
        make_choice(objs)

def make_objs(title, text, buttons):
    res = list(zip(title, text, buttons))
    lst = []
    count = 1
    for item in res:
        obj = SerRes()
        lst.append(obj)
        obj.text = item[0].text + '\n' + item[1].text
        obj.button = item[2] 
        obj.count = count
        count += 1
    return lst

