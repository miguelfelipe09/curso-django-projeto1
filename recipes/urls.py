from django.urls import path

from recipes.views import contato, home, sobre

urlpatterns = [
    path('home/', home),
    path('contato/', contato),
    path('sobre/', sobre),
]
