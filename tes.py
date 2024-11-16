from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

f_p = 'http://www.fantasypros.com/mlb/rankings/nl-only.php'


options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get(f_p)

f_p_holder = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div[2]/section/div/table/tbody/tr[30]/td[3]/div').text
print(f_p_holder)

'''f_p_ls = []

for players in f_p_holder:
    f_p_temp = players.text
    f_p_player = f_p_temp[:f_p_temp.index('(') - 1]
    f_p_ls.append(f_p_player)

driver.quit()

print(len(f_p_ls))'''


#/html/body/div[1]/div[3]/div/div[1]/div[2]/section/div/table/tbody/tr[30]/td[3]/div