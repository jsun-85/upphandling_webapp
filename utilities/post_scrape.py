import requests
import pandas as pd
import datetime as dt

url = 'https://gateway.pabliq.se/api/opensearchapi/v1/search'

def convert_to_date(column):
    return pd.to_datetime(column).dt.tz_localize(None).dt.strftime('%Y-%m-%d')


def fetch_data(url='https://gateway.pabliq.se/api/opensearchapi/v1/search', columns=None, **kwargs):

    search_json = {'langid':'sv',
                    'searchFields':{'freetxt':['vibrationer'], 'nutsCodes':['SE']},}
    if kwargs:
        fields = {k:v for k,v in kwargs.items()}
        search_json = {'langid':'sv',
                    'searchFields':fields,}

    r = requests.post(url, json=search_json)

    print(r.json())

    baselink = 'https://app.pabliq.se/procurements/'

    df = pd.DataFrame(r.json()['result'])

    df2 = pd.json_normalize(r.json()['result'])
    df2['link'] = baselink + df2['urlPath']
    df2.rename(columns={'title':'Upphandling', 'procurer.name': 'Beställare', 'published': 'Publicerat', 'deadline': 'Svara_senast', 'link': 'Länk'}, inplace=True)
    df2['Publicerat'] = convert_to_date(df2['Publicerat'])
    df2['Svara_senast'] = convert_to_date(df2['Svara_senast'])
    if  columns:
        df2 = df2[columns]

    return df2

if __name__ == '__main__':
    df = fetch_data(url, freetxt =['vibrationer'], nutsCodes=['SE'])