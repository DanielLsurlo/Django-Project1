from django.urls import path  # type:ignore

from recipes.views import home

urlpatterns = [
    path('', home),

]
