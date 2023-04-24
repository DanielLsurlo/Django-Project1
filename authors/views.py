import os

from django.contrib import messages  # type: ignore
from django.contrib.auth import authenticate, login, logout  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.http import Http404  # type: ignore
from django.shortcuts import redirect, render  # type: ignore
from django.urls import reverse  # type: ignore

from recipes.models import Recipe
from utils.pagination import make_pagination

from .forms import LoginForm, RegisterForm

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create')
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is Created, please log in. ')

        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()
    form = LoginForm(request.POST)
    login_url = reverse('authors:dashboard')

    if form.is_valid():
        authenticate_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticate_user is not None:
            messages.success(request, 'You are logged in.')
            login(request, authenticate_user)

        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect(login_url)


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('authors:login'))

    messages.success(request, 'Logout successfully')
    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'authors/pages/dashboard.html',
                  {
                      'recipes': page_obj,
                      'pagination_range': pagination_range,
                  }
                  )
