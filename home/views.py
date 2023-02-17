from django.shortcuts import render
from django.http import HttpResponse
from utilities import opic
from utilities import pabliq
from django.http import JsonResponse

def rows2_data(request):
    my_dataframe2 = pabliq.get_articles('vibration')
    my_dataframe2.columns = ['Upphandling', 'Beställare', 'Publicerat', 'Svara senast', 'Länk']
    rows2 = []

    for index, row in my_dataframe2.iterrows():
        Titel = row['Upphandling']
        Beställare = row['Beställare']
        Publicerat = row['Publicerat']
        Svara_senast = row['Svara senast']
        Länk = row['Länk']
        rows2.append({
            'Titel': Titel,
            'Beställare': Beställare,
            'Publicerat': Publicerat,
            'Svara_senast': Svara_senast,
            'Länk': Länk
        })

    return JsonResponse(rows2, safe=False)
# Create your views here.

# def index(request):
#
#     # Page from the theme
#     return render(request, 'pages/index.html')


# Create your views here.


def index(request):
    my_dataframe = opic.get_articles('vibration').T
    my_dataframe.columns = ['Titel', 'Beskrivning', 'Anbudstid', 'Länk']
    my_dataframe['Länk'] = my_dataframe['Länk'].apply(
        lambda x: '<a href="{0}">{0}</a>'.format(x))
    #
    # # my_dataframe = MyModel.objects.all()  # or however you're getting your data
    # context = {'my_dataframe': my_dataframe.to_html(escape=False, index=False)}
    rows = []
    for index, row in my_dataframe.iterrows():
        Titel = row['Titel']
        Beskrivning = row['Beskrivning']
        Anbudstid = row['Anbudstid']
        Länk = row['Länk']
        rows.append({
            'Titel': Titel,
            'Beskrivning': Beskrivning,
            'Anbudstid': Anbudstid,
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