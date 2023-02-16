import pandas as pd
from utilities import pabliq
from utilities import opic

print('Loading')

search_words = ['vibration', 'riskanalys', 'besiktning', 'syneförättning']

def create_table_rows(function, search_words, columns, transverse=False):
    dataframe_list = []
    print('Starting')
    print(dataframe_list)
    for search_word in search_words:
        print(search_word)
        dataframe_list.append(function(search_word))

    df = pd.concat(dataframe_list)
    if transverse:
        df = df.T
    print(df)
    df.columns = columns
    df['Länk'] = df['Länk'].apply(lambda x: '<a href="{0}">{0}</a>'.format(x))

    rows = []
    for index, row in df.iterrows():
        rows.append(dict(row))

    return rows

if __name__ == '__main__':
    print('This is main')
    print(create_table_rows(pabliq.get_articles, search_words, ['Upphandling', 'Beställare', 'Publicerat', 'Svara senast', 'Länk']))
    print(create_table_rows(opic.get_articles, search_words, ['Titel', 'Beskrivning', 'Anbudstid', 'Länk'], True))

    rows = create_table_rows(opic.get_articles, search_words, ['Upphandling', 'Beställare', 'Publicerat', 'Svara senast', 'Länk'], True)
    print(rows)
