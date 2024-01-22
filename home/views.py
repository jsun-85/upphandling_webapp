import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from utilities import opic
from utilities import pabliq
from django.http import JsonResponse
from utilities import post_scrape

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


def index(request):
    search_term = request.GET.get('search_term', starting_search_term)
    my_dataframe = opic.get_articles(search_term)
    my_dataframe = pd.concat([my_dataframe, post_scrape.fetch_data(columns=['Upphandling', 'Beställare', 'Publicerat',
                                                                       'Svara_senast', 'Länk'], freetxt =[starting_search_term], nutsCodes=['SE'])])
                                                                       'Svara_senast', 'Länk'], freetxt =[search_term], nutsCodes=['SE'])])
    my_dataframe['Länk'] = my_dataframe['Länk'].apply(
        lambda x: '<a href="{0}">{0}</a>'.format(x))
    my_dataframe = my_dataframe.dropna(subset=['Upphandling'])
    my_dataframe_sorted = my_dataframe.sort_values(by=['Publicerat'], ascending=False)
    print(my_dataframe_sorted)
    # # my_dataframe = MyModel.objects.all()  # or however you're getting your data
    # context = {'my_dataframe': my_dataframe.to_html(escape=False, index=False)}
    rows = []
    for index, row in my_dataframe_sorted.iterrows():
        Upphandling = row['Upphandling']
        Beställare = row['Beställare']
        Publicerat = row['Publicerat']
        Senast_svar = row['Svara_senast']
        Länk = row['Länk']
        rows.append({
            'Upphandling': Upphandling,
            'Beställare': Beställare,
            'Publicerat': Publicerat,
            'Senast_svar': Senast_svar,
            'Länk': Länk
        })

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
    if search_term:
        data = post_scrape.fetch_data(freetext=search_term, nutsCodes=['SE'])
        data_dict = data.to_dict('records')
        return JsonResponse({'rows': data_dict})
    else:
        return JsonResponse({'error': 'No search term provided'}, status=400)
