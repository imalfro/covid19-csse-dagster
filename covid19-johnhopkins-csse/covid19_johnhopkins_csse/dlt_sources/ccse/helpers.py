import re
import requests
from bs4 import BeautifulSoup

def extract():
    return 'a'

def get_csvs(dir):
    github_url = f'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/{dir}'  
    result = requests.get(github_url)
    soup = BeautifulSoup(result.text, 'html.parser')
    csvfiles = soup.find_all(title=re.compile("\.csv$"))
    print(csvfiles)
    #filename = []
    for i in csvfiles:
        df = extract('data', i['title'], i['href'].replace('/blob/','/refs/heads/'))
        yield df