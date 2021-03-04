from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from .models import Game, GameStats, Player
from .forms import GameForm, GameStatsForm, PlayerForm, AddGameForm


# Create your views here.

def get_home(request):
    # get 10 last games in db
    last_games_data = Game.objects.filter().order_by('-id')[:10]

    winner_scores = []

    # get scores of the last games

    for game in last_games_data:
        id = game.id
        winner = game.gagnant
        winner_stats = GameStats.objects.get(partie=id, joueur=winner)
        winner_scores.append(winner_stats)

    games_stats = zip(last_games_data, winner_scores)
    context = {
        "games_stats": games_stats,
    }
    return render(request, 'home.html', context)

def add_game(request):
    if request.method == 'POST':
        form = AddGameForm(request.POST)
        if form.is_valid():
            game_data = form.cleaned_data

            # get players - queryset
            player_1 = Player.objects.get(pk=int(game_data['joueur_1']))
            player_2 = Player.objects.get(pk=int(game_data['joueur_2']))

            # find winner
            if game_data['score_1'] > game_data['score_2']:
                winner = player_1
            else:
                winner = player_2

            # register game + update scores for players
            new_game = Game(
                date = game_data['date'],
                heure = game_data['heure'],
                lieu = game_data['lieu'],
                commentaires = game_data['commentaires'],
                gagnant = winner,
                )
            new_game.save()

            stats_joueur_1 = GameStats(
                joueur=player_1,
                partie=new_game,
                score=game_data['score_1'],
                nombre_scrabbles=game_data['nombre_de_scrabbles_1']
                )
            stats_joueur_1.save()

            stats_joueur_2 = GameStats(
                joueur=player_2,
                partie=new_game,
                score=game_data['score_2'],
                nombre_scrabbles=game_data['nombre_de_scrabbles_2']
                )
            stats_joueur_2.save()

            return redirect('game_detail', game_id=new_game.id)

    context = {
        'form': AddGameForm(),
    }
    return render(request, 'add_game.html', context)

def edit_game(request, pk):

    # get game by id
    game = Game.objects.get(id=pk)
    # get gamestats
    scores = GameStats.objects.filter(partie=pk)
    score_joueur_1 = GameStats.objects.get(partie=pk, joueur=scores[0].joueur.id)
    score_joueur_2 = GameStats.objects.get(partie=pk, joueur=scores[1].joueur.id)

    if request.method == 'POST':
        form = AddGameForm(request.POST)
        if form.is_valid():
            game_data = form.cleaned_data

            # get players - queryset
            player_1 = Player.objects.get(pk=int(game_data['joueur_1']))
            player_2 = Player.objects.get(pk=int(game_data['joueur_2']))

            # find winner
            if game_data['score_1'] > game_data['score_2']:
                winner = player_1
            else:
                winner = player_2

            # update game
            game.date = game_data['date']
            game.heure = game_data['heure']
            game.lieu = game_data['lieu']
            game.commentaires = game_data['commentaires']
            game.gagnant = winner
            game.save(update_fields=['date', 'heure', 'lieu', 'commentaires', 'gagnant'])

            # update players
            score_joueur_1.joueur=player_1
            score_joueur_1.score=game_data['score_1']
            score_joueur_1.nombre_scrabbles=game_data['nombre_de_scrabbles_1']
            score_joueur_1.save(update_fields=['joueur', 'score', 'nombre_scrabbles'])

           
            score_joueur_2.joueur=player_2
            score_joueur_2.score=game_data['score_2']
            score_joueur_2.nombre_scrabbles=game_data['nombre_de_scrabbles_2']
            score_joueur_2.save(update_fields=['joueur', 'score', 'nombre_scrabbles'])

            return redirect('game_detail', game_id=game.id)


    # initial state of the form 
    form = AddGameForm(initial= {
        'date': game.date,
        'heure': game.heure,
        'lieu': game.lieu,
        'joueur_1': scores[0].joueur.id,
        'score_1': scores[0].score,
        'nombre_de_scrabbles_1': scores[0].nombre_scrabbles,
        'joueur_2': scores[1].joueur.id,
        'score_2': scores[1].score,
        'nombre_de_scrabbles_2': scores[1].nombre_scrabbles,
        'commentaires': game.commentaires,
        }
        )
    context = {
        'form': form
    }
    return render(request, 'edit_game.html', context)



def get_game_list(request):

    # get games in db
    all_games = Game.objects.all().order_by('-date')

    stats_all_games = []

    # get scores of games
    for game in all_games:
        player_stats = GameStats.objects.filter(partie=game.id)
        stats_game = {
          'game': game,
          'player_stats': player_stats,
        }
        stats_all_games.append(stats_game)
    


    paginator = Paginator(stats_all_games, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "games": page_obj,
    }
    return render(request, 'list_games.html', context)



class PlayerList(ListView):
    model = Player
    template_name = 'list_players.html'
    context_object_name = 'players'
    ordering = ['nom']

    



class DeleteGame(DeleteView):
    model = Game
    template_name = 'delete_game.html'
    success_url = reverse_lazy('home')


def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save()
            player.save()
            return redirect('home')
    context = {
        'form': PlayerForm(),
    }
    return render(request, 'add_player.html', context)


def get_game_detail(request, game_id):

    # Get game stats in the database
    data = GameStats.objects.filter(partie=game_id)

    game_data = []

    for player in data:
        player_name = player.joueur.nom
        score = player.score
        scrabbles = player.nombre_scrabbles
        player_data = {
            'name': player_name,
            'score': score,
            'scrabbles': scrabbles
        }
        game_data.append(player_data)

    # Get infos of the game
    game = Game.objects.get(pk=game_id)

    context = {'game_scores': game_data, 'game': game,}
    return render(request, 'game_detail.html', context)


def get_player_stats(request, player_id):

    # get all games player by player
    games = GameStats.objects.filter(joueur=player_id)
    print(games)
    context = {'game': games}
    return render(request, 'player_stats.html', context)


def get_stats(request):

    # get all games + scores

    games = Game.objects.all()
    players_stats = GameStats.objects.all()

    high_score = 0
    scrabbles_hs = 0
    total_points = 0
 
    for stats in players_stats:
        # get high score + date 
        if stats.score > high_score:
            high_score = stats.score
            date_hs = stats.partie.date
            player_hs = stats.joueur
        # get scrabble record + date
        if stats.nombre_scrabbles > scrabbles_hs:
            scrabbles_hs = stats.nombre_scrabbles
            date_sc_hs = stats.partie.date
            player_sc_hs = stats.joueur
        total_points += stats.score

    mean_points_game_player = int(total_points / len(players_stats))
    mean_points_game = int(total_points / len(games))

    context = {
        'high_score': high_score,
        'date_hs': date_hs,
        'player_hs': player_hs,
        'scrabbles_hs': scrabbles_hs,
        'date_sc_hs': date_sc_hs,
        'player_sc_hs': player_sc_hs,
        'number_games': len(games),
        'mean_points_game_player': mean_points_game_player,
        'mean_points_game': mean_points_game,
    }
 
    return render(request, 'stats.html', context)