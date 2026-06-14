from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

data = []
base_url = 'https://www.hltv.org/ranking/teams'
years = [
    '/2026/january/5',
    '/2025/january/6', 
    '/2024/january/1', 
    '/2023/january/2',
    '/2022/january/3',
    '/2021/january/4',
    '/2020/january/6',
    '/2019/january/7',
    '/2018/january/1',
    '/2017/january/2',
    '/2016/march/28',
]

def get_year_clean(year: str) -> int:
    return int(year[1:5])

def get_region(country: str) -> str:
    
    country_clean = country.strip().lower()
    
    # Словарь соответствий: страна - регион
    region_map = {
        # === EUROPE ===
        'denmark': 'Europe', 'sweden': 'Europe', 'france': 'Europe',
        'germany': 'Europe', 'poland': 'Europe', 'spain': 'Europe',
        'portugal': 'Europe', 'italy': 'Europe', 'netherlands': 'Europe',
        'belgium': 'Europe', 'finland': 'Europe', 'norway': 'Europe',
        'czech republic': 'Europe', 'austria': 'Europe', 'switzerland': 'Europe',
        'united kingdom': 'Europe', 'england': 'Europe', 'scotland': 'Europe',
        'wales': 'Europe', 'ireland': 'Europe', 'romania': 'Europe',
        'hungary': 'Europe', 'slovakia': 'Europe', 'slovenia': 'Europe',
        'croatia': 'Europe', 'serbia': 'Europe', 'bosnia and herzegovina': 'Europe',
        'montenegro': 'Europe', 'north macedonia': 'Europe', 'bulgaria': 'Europe',
        'greece': 'Europe', 'turkey': 'Europe',
        'estonia': 'Europe', 'latvia': 'Europe', 'lithuania': 'Europe',
        'malta': 'Europe', 'cyprus': 'Europe', 'luxembourg': 'Europe',
        'iceland': 'Europe',
        
        # === CIS ===
        'russia': 'CIS', 'ukraine': 'CIS', 'belarus': 'CIS',
        'kazakhstan': 'CIS', 'georgia': 'CIS', 'armenia': 'CIS',
        'azerbaijan': 'CIS', 'moldova': 'CIS', 'kyrgyzstan': 'CIS',
        'tajikistan': 'CIS', 'turkmenistan': 'CIS', 'uzbekistan': 'CIS',
        
        # === NORTH AMERICA ===
        'united states': 'North America', 'usa': 'North America', 'canada': 'North America',
        'mexico': 'North America', 'guatemala': 'North America', 'dominican republic': 'North America',
        
        # === SOUTH AMERICA ===
        'brazil': 'South America', 'argentina': 'South America', 'chile': 'South America',
        'colombia': 'South America', 'peru': 'South America', 'uruguay': 'South America',
        'paraguay': 'South America', 'bolivia': 'South America', 'ecuador': 'South America',
        'venezuela': 'South America',
        
        # === ASIA ===
        'china': 'Asia', 'south korea': 'Asia', 'korea': 'Asia',
        'japan': 'Asia', 'india': 'Asia', 'thailand': 'Asia',
        'vietnam': 'Asia', 'philippines': 'Asia', 'indonesia': 'Asia',
        'malaysia': 'Asia', 'singapore': 'Asia', 'taiwan': 'Asia',
        'hong kong': 'Asia', 'mongolia': 'Asia', 'pakistan': 'Asia',
        'sri lanka': 'Asia', 'bangladesh': 'Asia', 'nepal': 'Asia',
        'myanmar': 'Asia', 'laos': 'Asia', 'cambodia': 'Asia',
        'brunei': 'Asia', 'timor-leste': 'Asia',
        'united arab emirates': 'Asia', 'lebanon': 'Asia',
        'jordan': 'Asia', 'iraq': 'Asia', 'syria': 'Asia',
        
        # === OCEANIA ===
        'australia': 'Oceania', 'new zealand': 'Oceania',
        'fiji': 'Oceania', 'papua new guinea': 'Oceania',
        'samoa': 'Oceania', 'tonga': 'Oceania',
        
        # === AFRICA ===
        'south africa': 'Africa',
    }
    
    return region_map.get(country_clean, 'Unknown')

# Parsing
print('=' * 30 + ' Parsing hltv.org ' + '=' * 30)

for year in years:
    time.sleep(3)
    response = requests.get(base_url + year)
    response.encoding = 'utf-8'
    
    bs = BeautifulSoup(response.text, 'html.parser')

    for tag in bs.find_all('div', {'class': 'ranked-team'})[:200]:

        ranking_position = int(tag.find('span', {'class': 'position wide-position'}).text[1:])

        for player in tag.find_all('td', {'class': 'player-holder'}):  
            
            nickname = player.find('div', {'class': 'nick'}).text
            country = player.find('img', {'class': 'flag'}).get('alt')
            
            player_data = {
                "player": nickname,
                "ranking_position": ranking_position,
                "country": country,
                "region": get_region(country),
                "year": get_year_clean(year)
            }
            
            data.append(player_data)

    print(year, 'parsed')

print('=' * 30 + ' Finished parsing ' + '=' * 30)

df = pd.DataFrame(data)

# Output
output_data_file = 'data/parsed-data.csv'
df.to_csv(output_data_file, index=False, encoding='utf-8')

print(f'Saved data to "{output_data_file}".')