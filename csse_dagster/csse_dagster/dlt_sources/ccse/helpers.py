import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = 'https://raw.githubusercontent.com'

def get_csvs(key, dir='', filenames=None):
    github_url = f'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/{dir}'  
    result = requests.get(github_url)
    if filenames:
        csvfiles = [ f'/CSSEGISandData/COVID-19/refs/heads/master/csse_covid_19_data/{dir}/{filename}'.replace('//','/') for filename in filenames ]
    else:
        soup = BeautifulSoup(result.text, 'html.parser')
        csvfiles = soup.find_all(title=re.compile("\.csv$"))
        csvfiles = [ i['href'].replace('/blob/','/refs/heads/') for i in csvfiles ]
    for i in csvfiles:
        chunksize = 10 ** 6
        print(f"extracting {key} from {BASE_URL}{i}")
        with pd.read_csv(f"{BASE_URL}{i}", dtype=object, index_col=False, chunksize=chunksize) as reader:
            for df_chunk in reader:
                print(f"extracted {df_chunk.shape[0]} rows x {df_chunk.shape[1]} cols")
                yield df_chunk

def get_timeseries_csvs(key, dir='', filenames=None, id_vars=None):
    github_url = f'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/{dir}'  
    result = requests.get(github_url)
    if filenames:
        csvfiles = [ [filename, f'/CSSEGISandData/COVID-19/refs/heads/master/csse_covid_19_data/{dir}/{filename}'.replace('//','/')] for filename in filenames ]
    else:
        soup = BeautifulSoup(result.text, 'html.parser')
        csvfiles = soup.find_all(title=re.compile(f"\.*{key}.*csv$"))
        csvfiles = [ [i['title'], i['href'].replace('/blob/','/refs/heads/')] for i in csvfiles ]
    for i in csvfiles:
        metric_col = i[0].replace('time_series_covid19_','').replace(f'_{key}.csv','')
        print(f"extracting {metric_col} in {key} files")
        chunksize = 10 ** 6
        with pd.read_csv(f"{BASE_URL}{i[1]}", dtype=object, index_col=False, chunksize=chunksize) as reader:
            for df_chunk in reader:
                #id_vars = [ col for col in id_vars if col in df_chunk.columns ]
                missing_cols = list(set(id_vars) - set(df_chunk.columns))
                df_chunk[missing_cols] = None
                df_chunk = pd.melt(df_chunk, id_vars=id_vars, var_name='date', value_name='cases')
                df_chunk['case_type'] = metric_col 
                print(f"extracted {df_chunk.shape[0] } rows x {df_chunk.shape[1]} cols")
                yield df_chunk