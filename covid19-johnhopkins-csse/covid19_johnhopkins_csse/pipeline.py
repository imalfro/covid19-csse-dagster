import re
import dlt
import requests
from bs4 import BeautifulSoup
from lib.extract import extract

@dlt.resource(
    table_name="issues",
    write_disposition="merge",
    primary_key="id",
)
def get_csvs(
        dir='csse_covid_19_daily_reports'
):
    github_url = f'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/{dir}'  
    result = requests.get(github_url)
    soup = BeautifulSoup(result.text, 'html.parser')
    csvfiles = soup.find_all(title=re.compile("\.csv$"))
    print(csvfiles)
    #filename = []
    for i in csvfiles:
        df = extract('data', i['title'], i['href'].replace('/blob/','/refs/heads/'))
        yield df

@dlt.source
def github_source():
    return get_csvs()