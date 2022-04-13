from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from const import *
from os.path import exists


#
# # функция download form:
# сначала находим ссылку на Для юр лиц, затем на Реабилитацию, а затем на нужный год. Если не получилось найти ссылки, используем альтернативный метод перехода на страницу "года"

def download_form(website, year):
    result = False

    initial_url = website + "/ru/"
    chrome_options = webdriver.ChromeOptions()
    abs_path = os.path.abspath("downloads")
    prefs = {'download.default_directory': abs_path}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(r"chromedriver.exe", chrome_options=chrome_options)
    driver.maximize_window()
    main_link = initial_url + add_url + str(year) + "-god"
    link = ""
    driver.get(initial_url)
    time.sleep(10)
    link_year_decision = ""
    result = get_link_yur(driver)
    if result:
        result = get_link_rehab(driver)
        if result:
            result, link_year_decision = get_link_year(driver, year)
            if result:
                main_link = link_year_decision
                print("Прошли первым методом")
    driver.get(main_link)

    print("Начинаем задание на сайте: " + main_link)

    link_download = ""
    file_path = ""
    try:

        # buttons = driver.find_elements(by=By.XPATH,value="//a[contains(text(), '%s') ][contains(text(), '%s')]" % (t, t2,))
        buttons = driver.find_elements(by=By.XPATH,
                                       value="//a[@title='Информационное сообщение' or @title='Информационные сообщения' ]")
        if len(buttons) == 0:
            buttons = driver.find_elements(by=By.XPATH,
                                           value="//a[contains(text(), '%s') ][contains(text(), '%s')]" % (t, t2,))

        if len(buttons) > 0:
            for button in buttons:
                if t3 == button.text or t4 == button.text or len(button.text) < 32:
                    link = button.get_attribute("href")

                    break

            print("Переходим на страницу (Информационные сооб): " + link)
            if "http" in link:
                driver.get(link)
                bool_continue = True
            else:
                print("Это не ссылка")
                bool_continue = False
        else:
            print("Не нашли Информационные сообщения")
            bool_continue = False

        if bool_continue:
            try:
                buttons = driver.find_elements(by=By.XPATH,
                                               value="//*[contains(text(),'%s') or contains(text(),'%s')]" % (
                                                   form_link_1, form_link_2))
                if len(buttons) > 0:
                    for button in buttons:

                        if button.get_attribute("href") is None:
                            print("href is none")
                            while button.get_attribute("href") is None and button is not None:
                                button = button.find_element(by=By.XPATH, value="./..")
                                # print(button.tag_name)
                                link_download = button.get_attribute("href")

                            break
                        else:
                            link_download = button.get_attribute("href")
                            break
                else:
                    print("Ничего не нашли")
                    result = False
                    return False, None
            except Exception as ex:
                print(ex)

            print("скачиваем файлы из (" + link_download + ")")
            if link_download is None or link_download == "" or "xls" not in link_download:
                print("Link не подходит = " + str(link_download) + " Не скачиваем")
                result = False
                return False
            driver.get(link_download)
            time.sleep(3)
            file_name = link_download.split("/")[-1]
            file_path = "downloads/" + file_name
            print(file_path)
            file_exists = exists(file_path)
            if file_exists:
                print(file_name)
                result = True

            else:
                print("Не скачалось. Битая ссылка. ")
                result = False
        else:
            print("Завершаем так как не смогли продолжить")
            result = False
        time.sleep(3)
    except Exception as ex:
        print(ex)
        result = False
    finally:
        driver.close()
        driver.quit()
        return result, file_path


def get_link_yur(driver):
    try:
        button = driver.find_element(by=By.XPATH,
                                     value="//a[contains(text(), '%s') ]" % (b))
        if b == button.text or b2 == button.text:
            link = button.get_attribute("href")
            driver.get(link)
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return False


def get_link_rehab(driver):
    result = False
    try:
        buttons = driver.find_elements(by=By.XPATH,
                                       value="//a[contains(text(), '%s') ]" % (c))
        for button in buttons:

            if c == button.text:
                link = button.get_attribute("href")
                driver.get(link)
                result = True
                break
        return result
    except Exception as ex:
        print(ex)
        return result


def get_link_year(driver, year):
    result = False
    link_year_decision = ""
    try:
        buttons = driver.find_elements(by=By.XPATH,
                                       value="//a[contains(text(), '%s') ]" % (str(year) + " год"))
        for button in buttons:

            if str(year) + " год" == button.text:
                link_year_decision = button.get_attribute("href")
        if link_year_decision != "":
            result = True
        if link_year_decision.split("/")[-1] != str(year) + "-god":
            print("Ссылка на год не берем: " + link_year_decision)
            result = False

        return result, link_year_decision
    except Exception as ex:
        print(ex)
