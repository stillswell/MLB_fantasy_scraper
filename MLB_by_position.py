from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

positions = ['c', '1b', '2b', '3b', 'ss', 'of', 'dh', 'sp', 'rp']
f_p = 'http://www.fantasypros.com/mlb/rankings/'
fp_end = '.php'

f_p_pos = []

for position in positions:

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(f_p+position+fp_end)

    f_p_holder = driver.find_elements(By.CLASS_NAME, 'player-cell.player-cell__td')

    f_p_ls = []

    for players in f_p_holder:
        f_p_temp = players.text
        f_p_player = f_p_temp[:f_p_temp.index('(') - 1]
        f_p_ls.append(f_p_player)

    driver.quit()

    f_p_pos.append(f_p_ls)
    print(len(f_p_ls))

f_p_pos_df = pd.DataFrame(f_p_pos)
f_p_pos_df = f_p_pos_df.transpose()
f_p_pos_df.columns = [positions]

