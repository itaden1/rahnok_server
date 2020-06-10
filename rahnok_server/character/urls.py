from django.urls import path, include

from character.views import character_web_view


urlpatterns = [
    path('get-characters/', character_web_view)
]


