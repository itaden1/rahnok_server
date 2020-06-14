from django.urls import path, include

from character.views import (
    character_web_view, 
    character_list_game_server_view, 
    character_detail_game_server_view,
    bulk_update_character_view
)


game_urls = [
    path('', bulk_update_character_view),
    path('user/', character_list_game_server_view),
    path('user/<slug:uuid>/', character_detail_game_server_view)
]

urlpatterns = [
    path('', character_web_view),
    path('game/', include(game_urls))
]


