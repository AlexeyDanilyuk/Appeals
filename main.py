import os

from selenium import webdriver


class FindAppeals:
    def __init__(self, reqvuch, katalog):
        self.reqvuch = reqvuch
        self.download_katalog = katalog

    def run(self):
        for numuch in self.reqvuch:

            link = f'http://{numuch}.hbr.msudrf.ru/admin.php'

            try:
                browser = webdriver.Chrome()
                browser.implicitly_wait(5)
                browser.get(link)

                browser.find_element_by_id('aid').send_keys(self.reqvuch[numuch][0])
                browser.find_element_by_id('pwd').send_keys(self.reqvuch[numuch][1])
                browser.find_element_by_class_name('but').click()

                browser.find_element_by_xpath('//a[text()="Обращения граждан"]').click()
                row = len(browser.find_elements_by_xpath('//table[@class="admList"]/tbody/tr/td[3]/nobr'))
                appeals_dict = {}

                for s in range(row):
                    if 'Проверка ЭП' in browser.find_element_by_xpath('//tr[' + str(s + 1) + ']/td[3]/nobr').text:
                        appeals_dict[browser.find_element_by_xpath(
                            '//tr[' + str(s + 1) + ']/td[2]/nobr').text] = browser.find_element_by_xpath(
                            '//tr[' + str(s + 1) + ']/td[4]/a').get_attribute('href')
                if appeals_dict:
                    for numappeals in appeals_dict:
                        download_path = f'{self.download_katalog}/{numuch}/{numappeals}'
                        if not os.path.isdir(download_path):
                            os.mkdir(download_path)
                        download_file_options = webdriver.ChromeOptions()
                        prefs = {"profile.default_content_settings.popups": 0,
                                 "download.default_directory": download_path.replace('/', '\\'),
                                 "directory_upgrade": True}
                        download_file_options.add_experimental_option("prefs", prefs)
                        browser = webdriver.Chrome(options=download_file_options)

                        browser.get(link)
                        browser.find_element_by_id('aid').send_keys(self.reqvuch[numuch][0])
                        browser.find_element_by_id('pwd').send_keys(self.reqvuch[numuch][1])
                        browser.find_element_by_class_name('but').click()
                        browser.get(appeals_dict[numappeals])
                        len_url_file = len(browser.find_elements_by_xpath('//a[@title="скачать файл"]'))
                        for link in range(len_url_file):
                            browser.find_elements_by_xpath('//a[@title="скачать файл"]')[link].click()
                        browser.find_elements_by_xpath('//input[@class="but"]')[0].click()
                        browser.quit()
                else:
                    print(f'По участку {numuch} нет новых обращений!')
            finally:
                browser.implicitly_wait(10)
                browser.quit()


if __name__ == '__main__':
    app = FindAppeals(
        {
            '44': ['user', 'password'],
            '45': ['user', 'password'],
            '46': ['user', 'password'],
            '74': ['user', 'password']
        },
        'каталог для сохранения',
    )
    app.run()
