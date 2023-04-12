from django.urls import path  # type: ignore

from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
]
