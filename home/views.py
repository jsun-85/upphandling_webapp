import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from utilities import opic
from utilities import pabliq
from django.http import JsonResponse
from utilities import post_scrape
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
    my_dataframe = opic.get_articles(search_term)
    print(f'opic: {my_dataframe}')
    fetched_data = post_scrape.fetch_data(columns=['Upphandling', 'Beställare', 'Publicerat', 'Svara_senast', 'Länk'], freetxt =[search_term], nutsCodes=['SE'])
    print(f'pabliq: {fetched_data}')
    if isinstance(fetched_data, dict):
        print(f"Error fetching data: {fetched_data}")
    else:
        my_dataframe = pd.concat([my_dataframe, fetched_data])

    my_dataframe['Länk'] = my_dataframe['Länk'].apply(
        lambda x: '<a href="{0}">{0}</a>'.format(x))
    my_dataframe = my_dataframe.dropna(subset=['Upphandling'])
    my_dataframe_sorted = my_dataframe.sort_values(by=['Publicerat'], ascending=False)
    print(my_dataframe_sorted)
    rows = []
    for index, row in my_dataframe_sorted.iterrows():
        Upphandling = row['Upphandling']
        Beställare = row['Beställare']
        Publicerat = row['Publicerat']
        Senast_svar = row['Senast_svar']
        Länk = row['Länk']
        rows.append({
            'Upphandling': Upphandling,
            'Beställare': Beställare,
            'Publicerat': Publicerat,
            'Senast_svar': Senast_svar,
            'Länk': Länk
        })
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
        return JsonResponse(rows, safe=False)
    else:
        return JsonResponse({'error': 'No search term provided'}, status=400)
