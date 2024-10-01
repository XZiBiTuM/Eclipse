import time
from datetime import datetime
from .models import *
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.views import LoginView


def article_list(request):
    articles = Article.objects.all()

    search_query = request.GET.get('search', '')
    sort_option = request.GET.get('sort', '')
    count = 0
    count_diff = 0

    if search_query:
        articles = articles.filter(title__icontains=search_query)
        count = articles.count()
        count_diff = count % 10

    if sort_option:
        articles = articles.order_by(sort_option)

    return render(request, 'article_list.html', {
        'articles': articles,
        'search_query': search_query,
        'sort_option': sort_option,
        'count': count,
        'count_diff': count_diff,
        'title': 'Список статей'
    })


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    verification = article.verification
    if verification:
        return render(request, 'article_detail.html', {'article': article, 'title': article.title})
    else:
        return redirect('article_list')


def create_article(request):
    plus_18_year_old = False
    current_user = request.user
    current_time_ms = int(time.time() * 1000)
    user_old_str = str(current_user.profile.birth_date).replace('-', '.')
    dt = datetime.strptime(user_old_str, "%Y.%m.%d")
    user_old_ms = int(dt.timestamp() * 1000)
    if current_time_ms - user_old_ms >= 568036800000:
        plus_18_year_old = True
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = current_user
            article.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ArticleForm()

    return render(request, 'create_article.html', {'form': form, 'old': plus_18_year_old})


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    if user != request.user:
        return redirect('profile', username=request.user.username)
    title = f"{user.username}#{user.id}"
    return render(request, 'profile.html', {'user': user, 'title': title})


@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)

    if user != request.user:
        return redirect('profile', username=user.username)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile', username=user.username)
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': f"{user.username} Редактирование",
    })


class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user.username})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} успешно создан!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form, 'title': 'Регистрация'})


def documentation_detail(request, pk):
    documentation = get_object_or_404(Documentation, pk=pk)
    return render(request, 'documentation_detail.html', {'documentation': documentation, 'title': documentation.title})


def documentation_list(request):
    documentations = Documentation.objects.all()

    search_query = request.GET.get('search', '')
    sort_option = request.GET.get('sort', '')
    count = 0
    count_diff = 0

    if search_query:
        documentations = documentations.filter(title__icontains=search_query)
        count = documentations.count()
        count_diff = count % 10

    if sort_option:
        documentations = documentations.order_by(sort_option)

    return render(request, 'documentation_list.html', {
        'documentations': documentations,
        'search_query': search_query,
        'sort_option': sort_option,
        'count': count,
        'count_diff': count_diff,
        'title': 'Справочник по Linux'
    })


def distro_detail(request, pk):
    distribution = get_object_or_404(LinuxDistribution, pk=pk)
    return render(request, 'distro_detail.html', {'distribution': distribution, 'title': distribution.name})


# def distros_list(request):
#     distributions = LinuxDistribution.objects.all()
#
#     search_query = request.GET.get('search')
#     if search_query:
#         distributions = distributions.filter(name__icontains=search_query)
#
#     sort_option = request.GET.get('sort')
#     if sort_option == 'name':
#         distributions = distributions.order_by('name')
#     elif sort_option == '-name':
#         distributions = distributions.order_by('-name')
#
#     selected_tag = request.GET.get('tag')
#     if selected_tag:
#         distributions = distributions.filter(tags__name=selected_tag)
#
#     tags = Tag.objects.all()
#
#     return render(request, 'distros_list.html', {
#         'distributions': distributions,
#         'tags': tags,
#         'selected_tag': selected_tag,
#         'search_query': search_query,
#         'sort_option': sort_option,
#         'title': 'Список дистрибутивов'
#     })


def distros_list(request):
    distributions = LinuxDistribution.objects.all()

    search_query = request.GET.get('search', '')
    sort_option = request.GET.get('sort', '')
    selected_tag = request.GET.get('tag', '')
    count = 0
    count_diff = 0

    if search_query:
        distributions = distributions.filter(name__icontains=search_query)
        count = distributions.count()
        count_diff = count % 10

    if selected_tag:
        distributions = distributions.filter(tags__name=selected_tag)

    if sort_option:
        distributions = distributions.order_by(sort_option)

    tags = Tag.objects.all()

    return render(request, 'distros_list.html', {
        'distributions': distributions,
        'tags': tags,
        'selected_tag': selected_tag,
        'search_query': search_query,
        'sort_option': sort_option,
        'count': count,
        'count_diff': count_diff,
        'title': 'Список дистрибутивов'
    })


def home(request):
    return render(request, 'base.html', {'title': 'Главная'})
