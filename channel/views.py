from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls.base import reverse

from channel.forms import ChannelForm, RegistrationForm, AuthorizationForm
from channel.models import Channel, Comment


def main(request):
    channels = Channel.objects.all()
    return render(request, 'channel/main.html', {'channels': channels})


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


def item(request, id):
    channel = Channel.objects.get(id=id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text is not None and len(text) > 0:
            Comment(author=request.user, text=text, channel=channel).save()
    return render(request, 'channel/item.html', {'channel': channel})


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
