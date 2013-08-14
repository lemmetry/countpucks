from django.http import HttpResponse
from django.shortcuts import render
from webservice.models import HockeyPlayer, Team
from django.views.decorators.csrf import csrf_exempt
import json


def homepage(request):
    # HockeyPlayer.objects.all().delete()
    # Team.objects.all().delete()

    teams = Team.objects.all()
    players = HockeyPlayer.objects.all()

    context = {'teams': teams,
               'players': players}
    return render(request, 'base.html', context)


def toJSON(dictionary):
    return json.dumps(dictionary, indent=2)


@csrf_exempt
def api(request):
    api_secret = '5e30d905-3aa0-4fe2-973f-e6268135631d'

    secret = request.POST.get('Secret')
    if secret != api_secret:
        return HttpResponse('Go awaaaaaaay...')
    else:
        full_name = request.POST.get('Full name')
        sweater = request.POST.get('Sweater')
        position = request.POST.get('Position')
        team = request.POST.get('Team')
        player_dict = {'full_name': full_name,
                       'sweater': sweater,
                       'position': position,
                       'team': team}
        json_player = toJSON(player_dict)

        try:
            team_name = Team.objects.get(team_name=team)
        except Team.DoesNotExist:
            team_name = Team.objects.create(team_name=team)

        try:
            player = HockeyPlayer.objects.get(full_name=full_name, team=team_name)
        except HockeyPlayer.DoesNotExist:
            player = HockeyPlayer(full_name=full_name, sweater=sweater, position=position)
            player.team = team_name
            player.save()

        return HttpResponse(json_player, content_type='application/json')