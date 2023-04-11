from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import date, timedelta
from selenium.webdriver import ActionChains
import pandas as pd
import re
import time
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import drive_connection


driver = webdriver.Chrome(executable_path="C:/Users/10126516/Documents/chromedriver.exe")
time.sleep(1)
driver.get("https://www.kap.org.tr/en/")
time.sleep(5)
driver.find_element(By.ID, "menu0").click()
time.sleep(1)
driver.find_element(By.ID , "submenu02230").click()
time.sleep(1)
# driver.find_element(By.CSS_SELECTOR, ".filter-singledropselect").click()

for elem in driver.find_elements(By.CLASS_NAME, "filter-singletext"):
    if elem.text == "All Indices":
        elem.click()

time.sleep(1)

for i in driver.find_elements(By.CLASS_NAME, "filter-singledropselect"):
    if i.text=="BIST ALL SHARES":
        i.click()

time.sleep(1)

for i in driver.find_elements(By.CLASS_NAME, "buttonLabel"):
    if i.text==" All Notifications":
        i.click()
        time.sleep(1)
        parent_element = i.find_element(By.XPATH, "..")
        sibling_element = parent_element.find_element(By.XPATH, "./following-sibling::*[1]")
        child_element = sibling_element.find_element(By.XPATH, "./child::*[2]")
        grand_child_element= child_element.find_element(By.XPATH, "./child::*[2]").click()

time.sleep(1)

# babasının ikinci oğlunun ikinci oğlunun oğlu
none_selected = driver.find_elements(By.CSS_SELECTOR, ".filter-multi.padding.right")[3]
none_selected.click()
time.sleep(1)
father = none_selected.find_element(By.XPATH, "..")
son = father.find_element(By.XPATH, "./child::*[2]")
second_son_of_son=son.find_element(By.XPATH, "./child::*[2]")
financial_report= second_son_of_son.find_element(By.XPATH, "./child::*[1]")
financial_report.click()

time.sleep(1)

driver.find_elements(By.CSS_SELECTOR, ".w-clearfix.column-type6.padding.bottom")[1].click()
time.sleep(1)


# babasının oğlunun oğlunun oğlunun 3.oğlu
çocuk = driver.find_elements(By.CLASS_NAME, "filter-singletext")[5]
çocuk.click()
time.sleep(1)
baba=çocuk.find_element(By.XPATH, "..")
oğlunun_oğlunun_oğlu = baba.find_element(By.XPATH, "./child::*[1]").find_element(By.XPATH, "./child::*[1]").find_element(By.XPATH, "./child::*[1]")
oğlunun_oğlunun_oğlu.get_attribute("Id")
üçüncü_oğul = oğlunun_oğlunun_oğlu.find_element(By.XPATH, "./child::*[4]").click()
time.sleep(1)


driver.find_element(By.CSS_SELECTOR, ".filter-button4.first").click()
time.sleep(5)


# =============================================================================
# 
# =============================================================================
finansallar = pd.DataFrame()
# finansallar = pd.read_csv("C:\\Users\\10126516\\Desktop\\Çalışmalar\\Selenium_Kodları/Hisseler.csv")
for idx, i in enumerate(driver.find_elements(By.CSS_SELECTOR, ".w-clearfix.notifications-row")):
    stock_quote = i.find_elements(By.XPATH, "./*")[1].find_elements(By.XPATH, "./*")[1].text
    print(idx)
    print(stock_quote)

    # print(i.index)
    try:
        i.click()
    except:
        driver.find_element(By.ID, "closeDisclosure").click()
        time.sleep(2)
        i.click()


    time.sleep(2)
    
    # Get page source and create soup object
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Extract data from general_role_210015-row-* classes
    import datetime
    
    başlangıç = datetime.datetime.now()
    # Extract data from general_role_210015-row-* classes
    data = []
    stock_quotes= []
    row_data = []
    temp_stock_quotes=[]
    rows = soup.find_all("tr", {"class": "presentation-enabled"})
    
    row_title_selector = ".gwt-Label.multi-language-content.content-en"
    taxonomy_footnote_value_selector = ".taxonomy-footnote-value"
    monetary_field_default_selector = ".monetary-field-default"

    for idx,row in enumerate(rows):
        taxonomy_footnote = rows[idx].select_one(taxonomy_footnote_value_selector)
        monetary_fields = rows[idx].select(monetary_field_default_selector)
        row_title = rows[idx].select_one(row_title_selector)
        
        taxonomy_footnote_value = taxonomy_footnote.text.strip()
        row_title_value = row_title.text.strip()
        if(len(monetary_fields)>0):
            col1_value = monetary_fields[0].text.strip()
            col2_value = monetary_fields[1].text.strip()
        data.append([row_title_value,taxonomy_footnote_value, col1_value, col2_value])
        
    for times in range(100):
        try:    
            currency = driver.find_element(By.CLASS_NAME, "financial-header-title").find_element(By.XPATH, "./following-sibling::*[1]").text
            break
        except:
            time.sleep(2)
            
        
    df = pd.DataFrame(data)
    df = df.assign(currency=currency)
    df = df.assign(stock_quote =stock_quote)
    finansallar = pd.concat([finansallar, df], axis=0)
    
    # drop rows with NaN in all columns except stock_quote
    finansallar.dropna(subset=finansallar.columns.difference(['stock_quote']), how='all', inplace=True)


    
    bitiş=datetime.datetime.now()
    print(başlangıç)
    print(bitiş)
    time.sleep(2)
    for times in range(100):
        try:
            driver.find_element(By.ID, "closeDisclosure").click()
            break
        except:
            time.sleep(10)

    time.sleep(2)


print(finansallar)
finansallar.to_csv("Hisseler.txt", index=False)

drive_connection.upload_to_drive('Hisseler.txt')
