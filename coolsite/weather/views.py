from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


class WeatherHome(DataMixin, ListView):

    paginate_by =  3
    model = Weather
    template_name = 'weather/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))
     #   context['menu'] = menu
     #   context['title'] = 'Главная страница'
     #   context['cat_selected'] = 0
     #   return context


    def get_queryset(self):
        return Weather.objects.filter(is_published=True).select_related('cat')
#def index(request):
##    posts = Weather.objects.all()
 #   if len(posts) == 0:
 #       raise Http404()

 #   context = {
 #       'posts': posts,
  #      'menu': menu,
  #      'title': 'Главная страница',
  #      'cat_selected': 0,
  #  }
  #  return render(request, 'weather/index.html', context=context)

def about(request):
    return render(request, 'weather/about.html', {'menu': menu, 'title': 'О сайте'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'weather/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


#def addpage(request):
#    if request.method == 'POST':
#        form = AddPostForm(request.POST, request.FILES)
#        if form.is_valid():
#            #print(form.cleaned_data)
#            form.save()
#            return redirect('home')
#    else:
#        form = AddPostForm()
#    return render(request, 'weather/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def internalServerError(request):
    return HttpResponse('<h1>Server error</h1>')


def pageBadRequest(request, *args, **argv):
    return HttpResponse('<h1>Bad request</h1>')

def pageNotAccess(request, *args, **argv):
    return HttpResponse('<h1>403-No access</h1>')


#def contact(request):
#        return HttpResponse("Обратная связь")

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'weather/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

#def login(request):
 #       return HttpResponse("Авторизация")



def pageNotFound(request, exception):
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class ShowPost(DataMixin, DetailView):
    model = Weather
    template_name = 'weather/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

#def show_post(request, post_slug):
#        post = get_object_or_404(Weather, slug=post_slug)
#
#        context = {
#           'post': post,
#            'menu': menu,
#            'title': post.title,
#            'cat_selected': post.cat_id,
#        }
#
#        return render(request, 'weather/post.html', context=context)


class WeatherCategory(DataMixin, ListView):
    model = Weather
    template_name = 'weather/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Weather.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

#def show_category(request, cat_id):
#    posts = Weather.objects.filter(cat_id=cat_id)
#
#    if len(posts) == 0:
#        raise Http404()
#    context = {
#        'posts': posts,
#        'menu': menu,
#        'title': 'Отображение по рубрикам',
#       'cat_selected': cat_id,
 #   }
  #  return render(request, 'weather/index.html', context=context)




class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'weather/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'weather/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
