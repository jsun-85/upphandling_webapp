from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('rows2-data/', views.rows2_data, name='rows2-data'),
]
