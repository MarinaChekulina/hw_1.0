from IPython.core.release import author
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.views import View
from pandas.io import json

from channel.forms import ChannelForm, RegistrationForm, AuthorizationForm
from channel.models import Channel, Comment, Like, Subscription
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# главная страница со списком каналов
def main(request):
    # по алфавиту по названиям
    channels = Channel.objects.all().order_by('title')
    # page = request.GET.get('page')
    # paginator = Paginator(channels, 3)
    # try:
    #     channels = paginator.page(page)
    # except PageNotAnInteger:
    #     channels = paginator.page(1)
    # except EmptyPage:
    #     channels = paginator.page(paginator.num_pages)
    return render(request, 'channel/main.html', {'channels': channels})


# заполнение формы для создания нового канала
@login_required
def new(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST, request.FILES)
        if form.is_valid():
            channel = Channel(**form.cleaned_data, author=request.user)
            channel.save()
            return redirect(reverse('item', args=[channel.id]))
    else:
        form = ChannelForm()
    return render(request, 'channel/new.html', {'form': form})


class SubscribeView(View):
    def post(self, request, id):
        if request.is_ajax():
            channel = Channel.objects.filter(id__exact=id)[0]
            users = channel.user_subscription.all()
            subscr = Subscription()
            subscr.user = request.user
            subscr.channel = channel
            subscr.save()
        # # user = request.user.username
        return HttpResponse(json.dumps({'message': request.user.username}))


class ChannelView(View):
    def get(self, request, id):
        channel = Channel.objects.filter(id__exact=id)[0]
        users = channel.user_subscription.all()
        form = ChannelForm()
        dictionary = {
            'channel': channel,
            'user': request.user.get_full_name(),
            'users': users,
            'form': form,
        }
        return render(request, 'channel/item.html', dictionary)


def add_channel1(request):
    if request.method == 'POST':
        channel = Channel()
        channel.title = request.POST.get('title')
        channel.category = request.POST.get('category')
        channel.image = request.FILES.get('image')
        channel.video = request.POST.get('video')
        channel.text = request.POST.get('text')
        channel.date = request.POST.get('date')
        channel.save()
        return HttpResponseRedirect('/item/{0}'.format(channel.id))
    return HttpResponseRedirect('/')


# добавление канала через модалку с валидацией js
def add_channel(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST, request.FILES)
        if form.is_valid():
            channel = Channel(**form.cleaned_data, author=request.user)
            channel.save()
            return redirect(reverse('item', args=[channel.id]))
    else:
        form = ChannelForm()
    return render(request, 'channel/new.html', {'form': form})


def item(request, id):
    channel = Channel.objects.get(id=id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text is not None and len(text) > 0:
            Comment(author=request.user, text=text, channel=channel).save()
    return render(request, 'channel/item.html', {'channel': channel})


class AddContent(View):
    def post(self, request):
        if request.is_ajax():
            last_channel_id = int(request.POST.get('last_channel_id'))
            channels = Channel.objects.all()
            if last_channel_id == channels.count():
                return HttpResponse(json.dumps({'message': 'stop'}))
            channel = channels[last_channel_id:last_channel_id + 1][0]
            data = {
                'channel_id': channel.id,
                'channel_image': channel.image.url,
                'channel_title': channel.title,
                'channel_text': channel.text
            }
            return HttpResponse(json.dumps({'message': data}))


# для регистрации нового пользователя
def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                auth_login(request, user)
            return redirect(reverse('main'))
    else:
        form = RegistrationForm()
    return render(request, 'channel/registration.html', {'form': form})


# для авторизации уже зарегистрированного пользователя
def login(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data.get('username'), password=data.get('password'))
            if user is not None:
                auth_login(request, user)
            return redirect(reverse('main'))
    else:
        form = AuthorizationForm()
    return render(request, 'channel/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect(reverse('main'))


# для лайков(рейтинг)
@login_required
def rate(request):
    try:
        ch_id = int(request.POST['tp'][1:])
        channel = Channel.objects.get(pk=ch_id)
        type = request.POST['tp'][0] == 'l'
        user = request.user
        like = Like.objects.filter(user=user, channel=channel).first()

        if like is None:
            if type:
                Like.objects.create(channel=channel, user=user, like=True)
                channel.rating += 1
            else:
                Like.objects.create(channel=channel, user=user, like=False)
                channel.rating -= 1

        elif like.like != type:
            if like.like:
                channel.rating -= 1
            else:
                channel.rating += 1
            like.delete()

        channel.save()
        return HttpResponse(json.dumps({
            'status': 'OK',
            'new': channel.rating,
        }), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({
            'status': 'error',
            'info': str(e),
        }), content_type='application/json')
