from django.urls import path  # type:ignore

from . import views

urlpatterns = [
    path('', views.home),
    path('recipes/<int:id>/', views.recipe),

]
