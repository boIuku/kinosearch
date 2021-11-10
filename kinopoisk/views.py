from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *

class KinopoiskHome(DataMixin, ListView):
    paginate_by = 3
    model = Kinopoisk
    template_name = 'kinopoisk/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Main Page")
        return context | c_def

def about(request):
    return render(request, 'kinopoisk/about.html')

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'kinopoisk/addpage.html', {'form':form, 'title': 'Adding page'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'kinopoisk/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add Page")
        return context | c_def

def contact(request):
    return render(request, 'kinopoisk/contact.html')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'kinopoisk/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Sign up")
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'kinopoisk/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Login")
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>NOT found</h1>")


class ShowPost(DataMixin, DetailView):
    model = Kinopoisk
    template_name = 'kinopoisk/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return context | c_def

class KinopoiskCategory(DataMixin, ListView):
    paginate_by = 3
    model = Kinopoisk
    template_name = 'kinopoisk/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Kinopoisk.objects.filter(cat__slug=self.kwargs['cat_slug'], watched=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Category - " + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return context | c_def

def wish_list(request):
    posts = Kinopoisk.objects.filter(watched=False)

    context = {
        'posts': posts,
        'title': 'Main Page',
        'cat_selected': 0,
        'watched':0,
    }
    return render(request, 'kinopoisk/index.html', context=context)
