from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
# from django.core.paginator import Paginator
# from django.urls import reverse_lazy

from news.models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from news.utils import MyMixin


def register(request):
    # Контроллер формы регистрации
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    # Контроллер формы Авторизации
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    # Обработчик ссылки "Выход"
    logout(request)
    return redirect('home')


def mail_sender(request):
    # Контроллер формы обратной связи
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'],
                             'mikhail.shchurovsky@gmail.com', ['total6@yandex.ru'],
                             fail_silently=True)
            if mail:
                messages.success(request, 'Письмо успешно отправлено!')
                return redirect('feedback')
            else:
                messages.error(request, 'Ошибка отправки!')
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = ContactForm()
    return render(request, 'news/feedback.html', {'form': form})


class HomeNews(MyMixin, ListView):
    """
       Контроллер для отображения новостей на главной
       странице сайта
    """
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    # extra_context = {'title': 'Главная'}
    mixin_prop = 'Новости для всех'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    """
    Контроллер для отображения новостей по
    категориям
    """
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'],
                                   is_published=True).select_related('category')


class ViewNews(DetailView):
    """
    Контроллер для отображения новости
    подробнее..
    """
    model = News
    # template_name = 'news/news_detail.html'
    # pk_url_kwarg = 'news_id'
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):
    """
    Контроллер формы создать новость
    """
    form_class = NewsForm
    template_name = 'news/add_news.html'
    raise_exception = True


# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей'
#     }
#     return render(request, template_name='news/index.html', context=context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})
#
#
# def view_news(request, news_id):
#     #news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {"news_item": news_item})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             #news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, "news/add_news.html", {'form': form})






