from django.urls import path, include

from auth_service.views import (
    auth_token_login_view,
    auth_logout_user_view,
    auth_token_verify_view,
    auth_logout_player_view
)

game_urls = [
    path('verify-token/', auth_token_verify_view),
    path('remove-player-token/', auth_logout_player_view),
]

urlpatterns = [
    path('retrieve-token/', auth_token_login_view),
    path('remove-user-token/<slug:uuid>/', auth_logout_user_view),
    path('game-auth/', include(game_urls)),
]


