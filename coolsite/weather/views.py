import requests
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .serializers import WeatherSerializer
from .forms import *
from weather.permissions import IsOwnerOrReadOnly
from .utils import *

class WeatherAPIList(generics.ListCreateAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

class WeatherAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
    permission_classes = (IsOwnerOrReadOnly, )


class WeatherAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer

    permission_classes = (IsAdminUser, )

# class WeatherViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.ListModelMixin,
#                    GenericViewSet):
#     queryset = Weather.objects.all()
#     serializer_class = WeatherSerializer
#
#
#     def get_queryset(self):
#         pk = self.kwargs.get("pk")
#
#         if not pk:
#             return Weather.objects.all()[:3]
#
#         return Weather.objects.filter(pk=pk)
#
#
#     @action(methods=['get'], detail=True)
#     def category(self, request, pk=None):
#         cats = Category.objects.get(pk=pk)
#         return Response({'cats': cats.name})
#
#
#
#
# class WeatherAPIList(generics.ListCreateAPIView):
#    queryset = Weather.objects.all()
#    serializer_class = WeatherSerializer
#
# class WeatherAPIUpdate(generics.UpdateAPIView):
#        queryset = Weather.objects.all()
#        serializer_class = WeatherSerializer
#
# class WeatherAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#        queryset = Weather.objects.all()
#        serializer_class = WeatherSerializer


#class WeatherAPIView(APIView):
#    def get(self, request):
 #       w = Weather.objects.all()
 #       return Response({'posts': WeatherSerializer(w, many=True).data})

  #  def post(self, request):
  #      serializer = WeatherSerializer(data=request.data)
  #      serializer.is_valid(raise_exception=True)

   #     post_new = Weather.objects.create(
   #         title=request.data['title'],
   #         content=request.data['content'],
   #         cat_id=request.data['cat_id']
   #     )

   #     return Response({'post': WeatherSerializer(post_new).data})

   # def put(self, request, *args, **kwargs):
   #     pk = kwargs.get("pk", None)
   #     if not pk:
   #         return Response({"error": "Method PUT not allowed"})

    #    try:
    #        instance = Weather.objects.get(pk=pk)
    #   except:
    #        return Response({"error": "Object does not exists"})

#        serializer = WeatherSerializer(data=request.data, instance=instance)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
 #       return Response({"post": serializer.data})

 #   def delete(self, request, *args, **kwargs):
 #       pk = kwargs.get("pk", None)
 #       if not pk:
 #           return Response({"error": "Method DELETE not allowed"})

        # здесь код для удаления записи с переданным pk

  #      return Response({"post": "delete post " + str(pk)})

#class WeatherAPIView(generics.ListAPIView):
#    queryset = Weather.objects.all()
#    serializer_class = WeatherSerializer

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
    appid = 'f3245c4c35e5cf5a0d069850d0a238a9'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    city = 'London'
    res = requests.get(url.format(city)).json()

    city_info = {
        'city': city,
        'temp': res["main"]["temp"],
        'icon': res["weather"][0]["icon"]
    }

    context = {'info': city_info}
    return render(request, 'weather/about.html', {'menu': menu, 'title': 'Получить информацию о погоде!'})

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

#def login(request):
 #   return HttpResponse("Авторизация")


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
