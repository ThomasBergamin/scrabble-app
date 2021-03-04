from django.forms import ModelForm
from django import forms
from .models import Game, GameStats, Player
import datetime

class GameForm(ModelForm):
	class Meta:
		model = Game
		fields = ['date', 'heure', 'lieu', 'commentaires','gagnant']

class GameStatsForm(ModelForm):
	class Meta:
		model = GameStats
		fields = ['joueur', 'partie', 'score', 'nombre_scrabbles']

class PlayerForm(ModelForm):
	class Meta:
		model = Player
		fields = ['nom']


class AddGameForm(forms.Form):

	# grab list of players
	players = Player.objects.all()
	player_choice = []
	for player in players:
		choice = (player.id, player.nom)
		player_choice.append(choice)

	now = datetime.datetime.now()
	YEARS = [x for x in range(2021,2025)]
	
	date = forms.DateField(widget=forms.SelectDateWidget(years=YEARS), initial=datetime.date.today)
	heure = forms.TimeField(initial=f"{now.hour}:{now.minute}",)
	lieu = forms.CharField()
	joueur_1 = forms.ChoiceField(choices=player_choice,)
	score_1 = forms.IntegerField()
	nombre_de_scrabbles_1 = forms.IntegerField()
	joueur_2 = forms.ChoiceField(choices=player_choice, initial=2)
	score_2 = forms.IntegerField()
	nombre_de_scrabbles_2 = forms.IntegerField()
	commentaires = forms.CharField(widget=forms.Textarea, required=False)