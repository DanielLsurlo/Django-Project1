from django.shortcuts import render  # type: ignore


def home(request):
    return render(request, 'recipes/pages/home.html', context={
        'name': 'Primeiro Nome'})
