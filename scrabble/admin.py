from django.contrib import admin
from .models import Game, GameStats, Player

# Register your models here.


admin.site.register(Game)
admin.site.register(GameStats)
admin.site.register(Player)