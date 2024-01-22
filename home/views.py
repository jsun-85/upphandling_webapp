import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from utilities import opic
from utilities import pabliq
from django.http import JsonResponse
from utilities import post_scrape
from django.core.serializers import serialize
import json

# def rows2_data(request):
#     my_dataframe2 = pabliq.get_articles('vibration')
#     my_dataframe2.columns = ['Upphandling', 'Beställare', 'Publicerat', 'Svara senast', 'Länk']
#     rows2 = []
#
#     for index, row in my_dataframe2.iterrows():
#         Titel = row['Upphandling']
#         Beställare = row['Beställare']
#         Publicerat = row['Publicerat']
#         Svara_senast = row['Svara senast']
#         Länk = row['Länk']
#         rows2.append({
#             'Titel': Titel,
#             'Beställare': Beställare,
#             'Publicerat': Publicerat,
#             'Svara_senast': Svara_senast,
#             'Länk': Länk
#         })
#
#     return JsonResponse(rows2, safe=False)
# Create your views here.

# def index(request):
#
#     # Page from the theme
#     return render(request, 'pages/index.html')

starting_search_term = 'vibration'

# Create your views here.


def fetch_and_process_data(search_term):
    print(f"Fetching and processing data for search term: {search_term}")
    print(f"Fetching and processing data for search term: {search_term}")
    print(f"Fetching and processing data for search term: {search_term}")
    my_dataframe = opic.get_articles(search_term)
    print(f'opic: {my_dataframe.shape[0]} rows')
    print(f'opic: {my_dataframe.shape[0]} rows')
    fetched_data = post_scrape.fetch_data(url=post_scrape.url, search_term=search_term)
    fetched_data = post_scrape.process_data(fetched_data)
    print(f'pabliq: {fetched_data.shape[0] if isinstance(fetched_data, pd.DataFrame) else 0} rows')
    print(f'pabliq: {fetched_data.shape[0] if isinstance(fetched_data, pd.DataFrame) else 0} rows')
    if isinstance(fetched_data, pd.DataFrame):
        my_dataframe = pd.concat([my_dataframe, fetched_data])
    else:
        print(f"Error fetching data: {fetched_data}")

    my_dataframe['Länk'] = my_dataframe['Länk'].apply(
        lambda x: '<a href="{0}">{0}</a>'.format(x))
    my_dataframe = my_dataframe.dropna(subset=['Upphandling'])
    my_dataframe_sorted = my_dataframe.sort_values(by=['Publicerat'], ascending=False)
    print(my_dataframe_sorted)
    rows = my_dataframe_sorted.to_dict(orient='records')
    # rows = []
    # for index, row in my_dataframe_sorted.iterrows():
    #     Upphandling = row['Upphandling']
    #     Beställare = row['Beställare']
    #     Publicerat = row['Publicerat']
    #     Senast_svar = row['Senast_svar']
    #     Länk = row['Länk']
    #     rows.append({
    #         'Upphandling': Upphandling,
    #         'Beställare': Beställare,
    #         'Publicerat': Publicerat,
    #         'Senast_svar': Senast_svar,
    #         'Länk': Länk
    #     })
    return rows

def index(request):
    search_term = request.GET.get('search_term', default=starting_search_term)
    rows = fetch_and_process_data(search_term)
    context = {'rows': rows}
    return render(request, 'pages/index.html', context)

# def rows2_data(request):
#     my_dataframe = pabliq.get_articles('vibration')
#     my_dataframe.columns = ['Upphandling', 'Beställare', 'Publicerat', 'Svara senast', 'Länk']
#     rows = []
#
#     for index, row in my_dataframe.iterrows():
#         Titel = row['Upphandling']
#         Beställare = row['Beställare']
#         Publicerat = row['Publicerat']
#         Svara_senast = row['Svara senast']
#         Länk = row['Länk']
#         rows.append({
#             'Titel': Titel,
#             'Beställare': Beställare,
#             'Publicerat': Publicerat,
#             'Svara_senast': Svara_senast,
#             'Länk': Länk
#         })
#
#     return JsonResponse(rows, safe=False)

def search_data(request):
    search_term = request.GET.get('search_term', '')
    print(search_term)
    if search_term:
        rows = fetch_and_process_data(search_term)
        rows = rows
        return JsonResponse({'rows': rows}, safe=False)
        # return JsonResponse(rows_json, safe=False)
    else:
        return JsonResponse({'error': 'No search term provided'}, status=400)
