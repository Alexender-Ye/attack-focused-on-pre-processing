import requests
from bs4 import BeautifulSoup
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager

DOMAIN = 'https://apkpure.com'
URL = 'https://apkpure.com/'
CATEGORY = 'communication'
DOWNLOAD_PATH = 'H:\\temp_application\\'
CHROMEDRIVER_PATH = 'F:\\third_part_command\\bin\\chromedriver.exe'

count = 0


def newest_suffix(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime).split(".")[-1]


def download_apks(url):
    driver1 = webdriver.Chrome(CHROMEDRIVER_PATH)
    driver1.get(url)
    soup = BeautifulSoup(driver1.page_source, "html.parser")
    # send the request
    #     soup = bs(requests.get(url, headers=headers).text, 'html.parser')
    # target divs
    target_divs = soup.findAll('div', {'class': 'category-template-down'})

    for div in target_divs:
        target_a = div.findAll("a")
        link = target_a[0].get('href')
        file_name = link.rsplit('/')[2]
        print('Downloading ' + file_name + '......')

        options = Options()
        options.add_experimental_option("prefs", {
            "download.default_directory": DOWNLOAD_PATH + CATEGORY
        })
        driver2 = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
        # enter download page
        driver2.get(DOMAIN + link)
        # download the apk
        soup = BeautifulSoup(driver2.page_source, "html.parser")
        try:
            target_divs_temp = soup.findAll('div', {'class': 'download-box'})
            temp_link = target_divs_temp[0].findAll("a")[0].get("href")
        except:
            print(target_divs_temp)

            driver2.quit()
            continue

        driver2.get(temp_link)
        # set the terminate varible
        termin_time = 0
        # use to determin the status of the download task
        flag = False
        time.sleep(1.5)
        while termin_time < 60:
            try:
                if "apk" not in newest_suffix(DOWNLOAD_PATH + CATEGORY):
                    time.sleep(5)
                    termin_time = termin_time + 1
                    continue
                else:
                    flag = True
                    break
            except:
                break

        driver2.quit()
        if flag:
            global count
            count += 1
            print(file_name + ": Successful")
        else:
            print(file_name + ": Failed")
    driver1.quit()


def iterate_page(base_url):
    driver = webdriver.Chrome(CHROMEDRIVER_PATH)
    driver.get(base_url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    max_page = int(soup.findAll('a', {'class': 'loadmore'})[0].get('data-maxpage')) + 1
    # page 13
    for page in range(1, 25):
        print("current page: " + str(page))
        target_url = base_url + '?page=' + str(page + 1)
        download_apks(target_url)

    print(str(count) + ' apks have been downloaded.')


    driver.quit()


def main():
    iterate_page(URL + CATEGORY)


if __name__ == "__main__":
    main()
