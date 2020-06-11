from django.urls import path, include

from character.views import character_web_view, character_list_game_server_view, character_detail_game_server_view


game_urls = [
    path('user/', character_list_game_server_view),
    path('user/<slug:uuid>/', character_detail_game_server_view)
]

urlpatterns = [
    path('', character_web_view),
    path('game/', include(game_urls))
]


