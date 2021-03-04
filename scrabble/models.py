from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class Player(models.Model):
    nom = models.CharField("Nom du joueur", max_length=30, unique=True)

    def __str__(self):
        return str(self.nom)


class Game(models.Model):
    date = models.DateField(default=timezone.now)
    heure = models.TimeField(default=timezone.now)
    lieu = models.CharField(max_length=30)
    commentaires = models.TextField(max_length=500, blank=True)
    gagnant = models.ForeignKey(Player, on_delete=models.CASCADE)


    def __str__(self):
        return f"Partie {str(self.pk)} : {str(self.date)}"

    def get_absolute_url(self):
        return reverse('game_detail', args=[str(self.id)])


class GameStats(models.Model):
    joueur = models.ForeignKey(Player, on_delete=models.CASCADE)
    partie = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        verbose_name_plural = "Gamestats's"

    class ScrabbleCount(models.IntegerChoices):
        Zero = 0
        Un = 1
        Deux = 2
        Trois = 3
        Quatre = 4
        Cinq = 5
        Six = 6
        Sept = 7
        Huit = 8
        Neuf = 9
        Dix = 10

    nombre_scrabbles = models.IntegerField(choices=ScrabbleCount.choices)

    def __str__(self):
        player_name = str(self.joueur)
        date = str(self.partie.date)
        heure = str(self.partie.heure)
        text_to_return = f"{player_name}, score : {self.score} , partie : {date} / {heure}"
        return text_to_return
