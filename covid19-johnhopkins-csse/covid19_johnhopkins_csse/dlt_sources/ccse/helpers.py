import re
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = 'https://raw.githubusercontent.com'

def extract(filename, file_url):
    data_url = f'{BASE_URL}{file_url}'

    with requests.get(data_url, stream=True) as r:
        r.raise_for_status()
        with open(f'./data/{filename}', 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    
    data = pd.read_csv(f'./data/{filename}')
    os.remove(f'./data/{filename}')
    #data = pd.melt(data, id_vars=['Province/State','Country/Region','Lat','Long'], var_name='date', value_name='confirmed')
    return data

def get_csvs(dir):
    github_url = f'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/{dir}'  
    result = requests.get(github_url)
    soup = BeautifulSoup(result.text, 'html.parser')
    csvfiles = soup.find_all(title=re.compile("\.csv$"))
    print(csvfiles)
    #filename = []
    for i in csvfiles:
        df = extract(f'{dir}_{i['title']}', i['href'].replace('/blob/','/refs/heads/'))
        yield df