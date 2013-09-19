from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from countpucks.webservice.models import HockeyPlayer, Team, PlayerScores, GoalieScores
import json


def data_from_db(request):
    teams = Team.objects.all().exclude(team_name='NO_TEAM')
    players = HockeyPlayer.objects.all()

    context = {'teams': teams,
               'players': players}
    return render(request, 'base.html', context)


def homepage(request):
    return render(request, 'homepage.html')


@csrf_exempt
def api(request):
    api_secret = '5e30d905-3aa0-4fe2-973f-e6268135631d'
    body = request.body
    player_dict = json.loads(body)

    if player_dict['Secret'] != api_secret:
        return HttpResponse('Go awaaaaaaay...')

    try:
        team_name = Team.objects.get(team_name=player_dict['Team'])
    except Team.DoesNotExist:
        team_name = Team.objects.create(team_name=player_dict['Team'])

    try:
        player = HockeyPlayer.objects.get(nhl_url=player_dict['NHL Url'])
    except HockeyPlayer.DoesNotExist:
        player = HockeyPlayer(nhl_url=player_dict['NHL Url'], full_name=player_dict['Full name'],
                              sweater=player_dict['Sweater'], position=player_dict['Position'],
                              birthdate=player_dict['Birthdate'])
        player.team = team_name
        player.save()

    if player_dict['Records available'] is False:
        return HttpResponse()

    if player_dict['Position'] != 'Goalie':
        # season = request.POST.get('Season')
        player_scores = PlayerScores(GP=player_dict['GP'], G=player_dict['G'], A=player_dict['A'], P=player_dict['P'],
                                     PlusMinus=player_dict['PlusMinus'], PIM=player_dict['PIM'], PP=player_dict['PP'],
                                     SH=player_dict['SH'], GWG=player_dict['GWG'], S=player_dict['S'],
                                     hits=player_dict['Hits'], BkS=player_dict['BkS'], GvA=player_dict['GvA'],
                                     TkA=player_dict['TkA'], TOIg=player_dict['TOIg'])
    else:
        # season = request.POST.get('Season')
        player_scores = GoalieScores(GP=player_dict['GP'], GS=player_dict['GS'], W=player_dict['W'], L=player_dict['L'],
                                     OT=player_dict['OT'], GA=player_dict['GA'], SA=player_dict['SA'],
                                     Sv=player_dict['Sv'], SvPercentage=player_dict['SvPercentage'],
                                     GAA=player_dict['GAA'], SO=player_dict['SO'], MIN=player_dict['Min'])
    player_scores.player = player
    player_scores.save()
    return HttpResponse()


# temporary func for testing/cleaning purposes
def deleteEverything(request):
    HockeyPlayer.objects.all().delete()
    Team.objects.all().delete()
    return HttpResponse()