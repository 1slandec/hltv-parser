from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

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
]

#   

data = []

def get_year(year_str):
    return int(year_str[1:5])

def get_region(country):
    
    # Приводим к нижнему регистру и убираем пробелы по краям
    country_clean = country.strip().lower()
    
    # Словарь соответствий: страна -> регион
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
        'united states': 'NA', 'usa': 'NA', 'canada': 'NA',
        'mexico': 'NA', 'guatemala': 'NA', 'dominican republic': 'NA',
        
        # === SOUTH AMERICA ===
        'brazil': 'SA', 'argentina': 'SA', 'chile': 'SA',
        'colombia': 'SA', 'peru': 'SA', 'uruguay': 'SA',
        'paraguay': 'SA', 'bolivia': 'SA', 'ecuador': 'SA',
        'venezuela': 'SA',
        
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
        
        # === AFRICA (добавлен отдельный регион) ===
        'south africa': 'Africa',
    }
    
    return region_map.get(country_clean, 'Unknown')

# Parsing
for year in years:
    time.sleep(3)
    response = requests.get(base_url+year)
    response.encoding = 'utf-8'
    
    bs = BeautifulSoup(response.text, 'html.parser')
    # data.append(bs)
    print(year, 'parsed')
    for tag in bs.find_all('div', {'class': 'ranked-team'}):
        for player in tag.find_all('td', {'class': 'player-holder'}):  
            
            nickname = player.find('div', {'class': 'nick'}).text
            country = player.find('img', {'class': 'flag'}).get('alt')
            
            player_data = {
                "nickname": nickname,
                "country": country,
                "year": get_year(year),
                'region': get_region(country)
            }
            
            data.append(player_data)


   
df = pd.DataFrame(data)

matrix_df = df.pivot_table(
    index='year',         
    columns='region',      
    values='nickname',    
    aggfunc='count',       
    fill_value=0           
)

matrix_df = matrix_df.sort_index()
matrix_df['Total'] = matrix_df.sum(axis=1)
# group = df.groupby(['region'])['nickname']
# agg_df = group.agg(total_players = 'count')


print(matrix_df)
# print(data)