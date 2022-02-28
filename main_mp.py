import multiprocessing
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from src.mail_send import send_mail

judicial_precinct = {
    '44': ['username', 'password', 'mail address'],
}

dir_path = 'L:\\Общая\\Обращения'
chrome_path_driver = os.path.join(os.getcwd(), 'chromedriver.exe')


def run_appeals_dict(numappeals, numuch, userid, passwd):
    download_path = os.path.join(dir_path, numuch, numappeals[0])
    os.makedirs(download_path, exist_ok=True)
    file_opt = webdriver.ChromeOptions()
    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": download_path,
        "directory_upgrade": True
    }
    file_opt.add_experimental_option("prefs", prefs)
    file_opt.add_argument('--headless')
    file_opt.add_argument('--verbose')
    file_opt.add_argument('--disable-software-rasterizer')
    browser = webdriver.Chrome(executable_path=chrome_path_driver, options=file_opt)
    browser.get(numappeals[1])

    browser.find_element(By.ID, 'aid').send_keys(userid)
    browser.find_element(By.ID, 'pwd').send_keys(passwd)
    browser.find_element(By.CLASS_NAME, 'but').click()

    browser.get(numappeals[1])
    len_url_file = len(browser.find_elements(By.XPATH, '//a[@title="скачать файл"]'))
    for url_file in range(len_url_file):
        browser.find_elements(By.XPATH, '//a[@title="скачать файл"]')[url_file].click()
        time.sleep(60)
    browser.find_element(By.XPATH, '//input[@class="but"]').click()


def loop_jp(data_jp):
    global browser
    userid = data_jp[1][0]
    passwd = data_jp[1][1]
    numuch = data_jp[0]
    email_uch = data_jp[1][2]

    link = f'http://{numuch}.hbr.msudrf.ru/admin.php'
    try:
        opt = Options()
        opt.add_argument('--headless')
        opt.add_argument('--verbose')
        opt.add_argument('--disable-software-rasterizer')

        browser = webdriver.Chrome(executable_path=chrome_path_driver, options=opt)
        browser.implicitly_wait(5)
        browser.get(link)

        browser.find_element(By.ID, 'aid').send_keys(userid)
        browser.find_element(By.ID, 'pwd').send_keys(passwd)
        browser.find_element(By.CLASS_NAME, 'but').click()

        browser.get(f'{link}?op=gbook_list_na')
        row = len(browser.find_elements(By.XPATH, '//table[@class="admList"]/tbody/tr/td[3]/nobr'))
        appeals_dict = {}

        for s in range(row):
            if 'Проверка ЭП' in browser.find_element(By.XPATH, '//tr[' + str(s + 1) + ']/td[3]/nobr').text:
                appeals_dict[browser.find_element(
                    By.XPATH, '//tr[' + str(s + 1) + ']/td[2]/nobr').text] = browser.find_element(
                    By.XPATH, '//tr[' + str(s + 1) + ']/td[4]/a').get_attribute('href')
        if appeals_dict:
            [multiprocessing.Process(target=run_appeals_dict,
                                     args=(numappeals, numuch, userid, passwd,)).start()
             for numappeals in appeals_dict.items()]
            if str(len(appeals_dict)).endswith('1') and len(appeals_dict) != 11:
                end_str = 'е'
            elif len(appeals_dict) % 10 in (2, 3, 4) and len(appeals_dict) not in (12, 13, 14):
                end_str = 'я'
            else:
                end_str = 'й'
            appeals_str = f'обращени{end_str}'
            print(f'По участку {numuch} найдено {len(appeals_dict)} {appeals_str}!')
            email_body = f'В систему обращений судебного участка №{numuch} поступило {len(appeals_dict)} ' \
                         f'{appeals_str}.\nКаталог с обращениями находится по адресу ' \
                         f'{os.path.join(dir_path, numuch)}'
            send_mail(email_uch, 'Оповещение об обращениях', email_body)
        else:
            print(f'По участку {numuch} нет новых обращений!')

    finally:
        browser.implicitly_wait(60)
        browser.quit()


if __name__ == '__main__':
    PROC = [multiprocessing.Process(target=loop_jp, args=(jp,)).start() for jp in judicial_precinct.items()]
