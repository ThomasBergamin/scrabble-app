from django.urls import path
from .views import PlayerList, DeleteGame
from . import views

urlpatterns = [
    path('', views.get_home, name='home'),
    path('games/', views.get_game_list, name='games'),
    path('games/details/<game_id>', views.get_game_detail, name='game_detail'),
    path('games/new_game/', views.add_game, name='add_game'),
    path('new_player/', views.add_player, name='add_player'),
    path('games/edit/<int:pk>', views.edit_game, name='edit_game'),
    path('delete/<int:pk>', DeleteGame.as_view(), name='delete_game'),
    path('players/', PlayerList.as_view(), name='list_players'),
    path('players/stats/<player_id>', views.get_player_stats, name='get_stats'),
    path('stats/', views.get_stats, name='stats'),
]