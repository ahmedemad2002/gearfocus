from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

MAIN_PAGE_TIMEOUT = 15

def driver_init():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(MAIN_PAGE_TIMEOUT)
    driver.maximize_window()
    return driver

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8' ) as file:
        data = json.load(file)
    return data

def seller_data(driver, url):
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.text-input.font-semibold.text-brand-blue"))
        )
    except Exception as e:
        print("Timed out waiting for element to be present")
        raise  # Reraise the exception to handle it in the calling script

    link = element
    seller_name, seller_url = link.get_attribute('text'), link.get_attribute("href")
    print(seller_name, seller_url)
    return seller_name, seller_url

def update_item_using_driver(item, driver):
    try:
        seller_name, seller_url = seller_data(driver, item['item_url'])
    except Exception as e:
        seller_name, seller_url = None, None
        print(f'Failed getting data from {item["item_url"]} with error {e}')
    item['seller_name'] = seller_name
    item['seller_url'] = seller_url
    return item

def update_file(file_path):
    data = read_json('data/curr_run.json')
    sellers_dict = read_json('Scripts/Env Data/Sellers_dictionary.json')
    driver = driver_init()
    for item in data:
        if item['seller_id'] in sellers_dict:
            item['seller_name'] = sellers_dict[item['seller_id']]['name']
            item['seller_url'] = sellers_dict[item['seller_id']]['url']
        else:
            item = update_item_using_driver(item, driver)
            if item['seller_name'] is not None:
                sellers_dict[item['seller_id']] = {'name': item['seller_name'], 'url': item['seller_url']}
    driver.quit()
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
    with open('Scripts/Env Data/Sellers_dictionary.json', 'w') as file:
        json.dump(sellers_dict, file, indent=2)
    
