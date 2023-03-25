from django.shortcuts import render  # type: ignore


def home(request):
    return render(request, 'recipes/pages/home.html', context={
        'name': 'Primeiro Nome'})


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={
        'name': 'Primeiro Nome'})
