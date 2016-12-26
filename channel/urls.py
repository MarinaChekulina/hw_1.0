from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from channel.views import login, logout
from channel.views import main, item, new, registration
from hw import settings

urlpatterns = [
                  url(r'^$', main, name='main'),
                  url(r'^new$', new, name='new'),
                  url(r'^item/(?P<id>\d+)$', item, name='item'),
                  url(r'^registration/', registration, name='registration'),
                  url(r'^login/', login, name='login'),
                  url(r'^logout/', logout, name='logout'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
