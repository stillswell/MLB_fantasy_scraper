from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

#NL team abbreviation list
#yahoo and roto don't have NL filter options
#NL = 'ARI', 'ATL', 'CHC', 'CIN', 'MIA', 'LAD', 'MIL', 'NYM', 'PHI', 'PIT', 'SAD', 'SF', 'WSH', 'STL', 'COL'
NL = 'ARI|ATL|CHC|CIN|MIA|LAD|MIL|NYM|PHI|PIT|SAD|SF|WSH|STL|COL'

#webpage strings
#f_p = 'http://www.fantasypros.com/mlb/rankings/nl-only.php'
yahoo = 'https://sports.yahoo.com/mlb/fantasy-rankings/'
roto = 'https://www.rotochamp.com/'
r_b = 'https://www.rotoballer.com/fantasy-baseball-rankings/440514#!/rankings?spreadsheet=nl-only&league=Overall'


#f_p only reading out 25 players
'''#opening fantasypros and scraping data
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get(f_p)
f_p_holder = driver.find_elements(By.CLASS_NAME, 'player-cell.player-cell__td')
f_p_df = []

for players in f_p_holder:
    row = players.text
    f_p_df.append(row)

driver.quit()

#converting to Dataframe and cleaning
f_p_df = pd.DataFrame(f_p_df)
f_p_df.columns = ['Player']
f_p_df[['Player','Team']] = f_p_df['Player'].str.split('(', expand=True)
f_p_df['Team'] = f_p_df['Team'].str.replace(')', '')
f_p_df['Score'] = 100 - f_p_df.index'''


#opening yahoo and scraping data
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get(yahoo)

yahoo_player = []
yahoo_team = []

i=1
while i < 424:
    i = str(i)
    p_path = '/html/body/div[1]/div/div/div/div/div[3]/div[1]/div/div/div/div/div/div[2]/table/tbody/tr[' + i + ']/td[2]/a/div/span/span[1]'
    t_path = '/html/body/div[1]/div/div/div/div/div[3]/div[1]/div/div/div/div/div/div[2]/table/tbody/tr[' + i + ']/td[2]/a/div/span/span[2]'
    player_holder = driver.find_element(By.XPATH, p_path).text
    yahoo_player.append(str(player_holder))
    team_holder = driver.find_element(By.XPATH, t_path).text
    yahoo_team.append(str(team_holder))
    i = int(i)
    i += 1

driver.quit()

#converting to Dataframe and cleaning
yahoo_df = {'Player' : yahoo_player,
            'Team' : yahoo_team}

yahoo_df = pd.DataFrame(yahoo_df)
yahoo_df[['Team', 'Position']] = yahoo_df['Team'].str.split(' ', expand=True)
yahoo_df.drop('Position', axis=1, inplace=True)
yahoo_df = yahoo_df[yahoo_df['Team'].str.contains(NL) == True]
yahoo_df = yahoo_df.reset_index(drop=True)
yahoo_df = yahoo_df.iloc[0:100]
yahoo_df['Score'] = 100 - yahoo_df.index


#opening roto champ and scraping data
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get(roto)

roto_player = []
roto_team = []

i = 0
while i < 300:
    i = str(i)
    player = '//*[@id="MainContent_gridProjections_linkPlayerStats_' + i + '"]'
    team = '//*[@id="MainContent_gridProjections_linkTeam_' + i + '"]'
    player_holder = driver.find_element(By.XPATH, player).text
    team_holder = driver.find_element(By.XPATH, team).text
    roto_player.append(player_holder)
    roto_team.append(team_holder)
    i = int(i)
    i += 1

roto_df = {'Player' : roto_player,
            'Team' : roto_team}

roto_df = pd.DataFrame(roto_df)
driver.quit()

roto_df = roto_df[roto_df['Team'].str.contains(NL) == True]
roto_df = roto_df.reset_index(drop=True)
roto_df = roto_df.iloc[0:100]
roto_df['Score'] = 100 - roto_df.index

#opening roto baller and scraping data
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get(r_b)

r_b_player = []
r_b_team = []

i = 1
while i < 101:
    i = str(i)
    player = 'tr.ng-scope:nth-child('+i+') > td:nth-child(3) > span:nth-child(1) > a:nth-child(1)'
    player_holder = driver.find_element(By.CSS_SELECTOR, player).text
    r_b_player.append(player_holder)
    i = int(i)
    i += 1

r_b_df = pd.DataFrame(r_b_player)
driver.quit()

r_b_df.columns = ['Player']
r_b_df['Score'] = 100 - r_b_df.index


#combining overall lists
overall = pd.concat([yahoo_df, roto_df, r_b_df], ignore_index=True)
overall = overall.groupby('Player')[['Score']].sum()
overall = overall.sort_values('Score', ascending=False)
print(overall)
