import requests
import pandas as pd
import datetime as dt
import dateutil as du

url = 'https://gateway.pabliq.se/api/opensearchapi/v1/search'

def du_parser(str):
    return du.parser.parse(str).date()

def ts_parser(str):
    return pd.to_datetime(str, unit='D')
def convert_to_date(column):
    # for value in column:
    #     print(type(value))
    # column2 = pd.to_datetime(column, format='ISO8601')
    # for value in column2:
    #     print(type(value))
    # return column.apply(dt.datetime.fromtimestamp)
    # return column.apply(ts_parser)
    return pd.to_datetime(column, format='ISO8601').dt.tz_localize(None).dt.strftime('%Y-%m-%d')
    return pd.to_datetime(column, unit='D').dt.tz_localize(None).dt.strftime('%Y-%m-%d')


def fetch_data(url='https://gateway.pabliq.se/api/opensearchapi/v1/search', search_term='tekniska konsulter', **kwargs):

    print(kwargs)

    search_json = {'langid':'sv',
                    'searchFields':{'freetxt':[search_term], 'nutsCodes':['SE']},}

    try:
        r = requests.post(url, json=search_json)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        return {"error": "HTTP Error"}
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        return {"error": "Connection Error"}
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        return {"error": "Timeout Error"}
    except requests.exceptions.RequestException as err:
        print ("Something went wrong with the request:",err)
        return {"error": "Request Error"}

    return r.json()

def process_data(json_data, columns=['Upphandling', 'Beställare', 'Publicerat', 'Svara_senast', 'Länk']):
    baselink = 'https://app.pabliq.se/procurements/'

    if 'result' in json_data:
        df = pd.DataFrame(json_data['result'])
    else:
        print("Error: 'result' not found in json_data")
        return pd.DataFrame()

    df2 = pd.json_normalize(json_data['result'])
    df2['link'] = baselink + df2['urlPath']
    df2.rename(columns={'title':'Upphandling', 'procurer.name': 'Beställare', 'published': 'Publicerat', 'deadline': 'Svara_senast', 'link': 'Länk'}, inplace=True)
    df2['Publicerat'] = convert_to_date(df2['Publicerat'])
    df2['Svara_senast'] = convert_to_date(df2['Svara_senast'])
    if columns:
        df2 = df2[columns]
    print(df2)
    return df2

if __name__ == '__main__':

    df = fetch_data(url, freetxt =['vibrationer'], nutsCodes=['SE'])
