from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from countpucks.webservice.models import HockeyPlayer, Team, PlayerScores, GoalieScores
import json


def homepage(request):
    teams = Team.objects.all().exclude(team_name='NO_TEAM')
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
        nhl_url = request.POST.get('NHL Url')
        full_name = request.POST.get('Full name')
        sweater = request.POST.get('Sweater')
        position = request.POST.get('Position')
        team = request.POST.get('Team')
        birthdate = request.POST.get('Birthdate')
        records_available = request.POST.get('Records available')
        # print(full_name, records_available)

        try:
            team_name = Team.objects.get(team_name=team)
        except Team.DoesNotExist:
            team_name = Team.objects.create(team_name=team)

        try:
            player = HockeyPlayer.objects.get(nhl_url=nhl_url)
        except HockeyPlayer.DoesNotExist:
            player = HockeyPlayer(nhl_url=nhl_url, full_name=full_name, sweater=sweater, position=position, birthdate=birthdate)
            player.team = team_name
            player.save()

        if str(records_available) == 'False':
            return HttpResponse()
        else:
            if position != 'Goalie':
                # season = request.POST.get('Season')
                GP = request.POST.get('GP')
                G = request.POST.get('G')
                A = request.POST.get('A')
                P = request.POST.get('P')
                PlusMinus = request.POST.get('PlusMinus')
                PIM = request.POST.get('PIM')
                PP = request.POST.get('PP')
                SH = request.POST.get('SH')
                GWG = request.POST.get('GWG')
                S = request.POST.get('S')
                Hits = request.POST.get('Hits')
                BkS = request.POST.get('BkS')
                GvA = request.POST.get('GvA')
                TkA = request.POST.get('TkA')
                TOIg = request.POST.get('TOIg')

                player_scores = PlayerScores(GP=GP, G=G, A=A, P=P, PlusMinus=PlusMinus, PIM=PIM, PP=PP, SH=SH,
                                             GWG=GWG, S=S, hits=Hits, BkS=BkS, GvA=GvA, TkA=TkA, TOIg=TOIg)
                player_scores.player = player
                player_scores.save()
            else:
                # season = request.POST.get('Season')
                GP = request.POST.get('GP')
                GS = request.POST.get('GS')
                W = request.POST.get('W')
                L = request.POST.get('L')
                OT = request.POST.get('OT')
                GA = request.POST.get('GA')
                SA = request.POST.get('SA')
                Sv = request.POST.get('Sv')
                SvPercentage = request.POST.get('SvPercentage')
                GAA = request.POST.get('GAA')
                SO = request.POST.get('SO')
                Min = request.POST.get('Min')

                player_scores = GoalieScores(GP=GP, GS=GS, W=W, L=L, OT=OT, GA=GA, SA=SA, Sv=Sv, SvPercentage=SvPercentage,
                                             GAA=GAA, SO=SO, MIN=Min)
                player_scores.player = player
                player_scores.save()

            return HttpResponse()


# temporary func for testing/cleaning purposes
def deleteEverything(request):
    HockeyPlayer.objects.all().delete()
    Team.objects.all().delete()
    return HttpResponse()