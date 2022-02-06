import pandas as pd
import requests
import urllib
import enum
from bs4 import BeautifulSoup
import re

class TradeType(enum.Enum):
    IMPORT='Importer'
    EXPORT='Exporter'

def get_countries_by_product( type_:TradeType, hs4:int, year=2019 ):
    url = 'https://oec.world/olap-proxy/data'
    params = {
        'cube':'trade_i_baci_a_92',
        'HS4':str(hs4),
        'Year':str(year),
        'drilldowns':'{} Country'.format(type_.value),
        'locale':'en',
        'measures':'Trade Value',
        'parents':'true',
        'parse':'false',
        'properties':'{} Country ISO 3'.format(type_.value),
    }
    res = requests.get(url, params=params)
    if res.status_code == 404:
        return None
    res.raise_for_status()
    res_df = pd.DataFrame(
        res.json()['data']
    ).sort_values('Trade Value').iloc[::-1]
    trade_sum = res_df['Trade Value'].sum()
    res_df['Trade Percent'] = res_df['Trade Value'] / trade_sum
    return res_df
 
def search_hs4( query:str ):
    query = '-'.join(query.split(' '))
    hs4 = None
    try:
        res = requests.get('https://oec.world/en/profile/hs92/{}'.format(query))
        soup = BeautifulSoup(res.text)
        r = re.compile(r'Explore Visualizations')
        hs4 = int([x['href'].split('/')[8] for x in soup.find_all('a', text= r) ][0])
    except:
        pass
    return hs4


def generate_params_from_url(url):
    parse_result = urllib.parse.urlparse(url)
    query = parse_result.query
    params = dict(x.split('=') for x in query.split('&'))
    params = {k:' '.join(v.split('+')) for k,v in params.items()}
    return params


if __name__ == '__main__':
    for product in ['soybeans', 'crude petroleum', 'raw copper']:
        
        hs4 = search_hs4(product)
        print(product, hs4)
        
        import_df = get_countries_by_product( TradeType.IMPORT, hs4 = hs4, year=2020 )
        export_df = get_countries_by_product( TradeType.EXPORT, hs4 = hs4, year=2020 )
        
        print('IMPORTS')
        print(import_df.head())
        print('EXPORTS')
        print(export_df.head())
        
        print()
