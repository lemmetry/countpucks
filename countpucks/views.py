from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from countpucks.webservice.models import HockeyPlayer, Team, PlayerScores, GoalieScores
import json
import datetime
from django.core.paginator import Paginator


@csrf_exempt
def api(request):
    api_secret = '947e72de-b090-4979-83a8-fad44b4be3f5'
    player_dict = json.loads(request.body.decode(encoding='UTF-8'))

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
        player_scores = PlayerScores(Season=player_dict['Season'], GP=player_dict['GP'], G=player_dict['G'],
                                     A=player_dict['A'], P=player_dict['P'], PlusMinus=player_dict['PlusMinus'],
                                     PIM=player_dict['PIM'], PP=player_dict['PP'], SH=player_dict['SH'],
                                     GWG=player_dict['GWG'], S=player_dict['S'], hits=player_dict['Hits'],
                                     BkS=player_dict['BkS'], GvA=player_dict['GvA'], TkA=player_dict['TkA'],
                                     TOIg=player_dict['TOIg'])
    else:
        player_scores = GoalieScores(Season=player_dict['Season'], GP=player_dict['GP'], GS=player_dict['GS'],
                                     W=player_dict['W'], L=player_dict['L'], OT=player_dict['OT'], GA=player_dict['GA'],
                                     SA=player_dict['SA'], Sv=player_dict['Sv'], SvPercentage=player_dict['SvPercentage'],
                                     GAA=player_dict['GAA'], SO=player_dict['SO'], MIN=player_dict['Min'])
    player_scores.player = player
    player_scores.save()
    return HttpResponse()


# temporary func for testing/cleaning purposes
def deleteEverything(request):
    HockeyPlayer.objects.all().delete()
    Team.objects.all().delete()
    return HttpResponse()


def playerOfTheDay(request):

    def applyFilters(players):
        goalies_with_records = players.filter(position='Goalie').exclude(goaliescores__isnull=True).filter(goaliescores__Season='2013-2014 REGULAR SEASON')
        players_with_records = players.exclude(position='Goalie').exclude(playerscores__isnull=True).filter(playerscores__Season='2013-2014 REGULAR SEASON')
        all_players_with_records = goalies_with_records | players_with_records

        players_with_number = all_players_with_records.exclude(sweater='NO_NUMBER')
        players_with_number_and_team = players_with_number.exclude(team__team_name='NO_TEAM')
        return players_with_number_and_team

    all_players = HockeyPlayer.objects.all()
    selected_players = applyFilters(all_players)

    p = Paginator(selected_players, 1)
    f = lambda i: (37 * i + 13) % p.num_pages

    today = datetime.date.today()
    today_int = int(today.strftime('%Y%m%d'))

    random_page_number = f(today_int)+1
    random_page = p.page(random_page_number)
    random_player = random_page.object_list[0]

    position = random_player.position

    if position != 'Goalie':
        template_name, context = getContextToPlotPlayer(random_player)
    else:
        template_name, context = getContextToPlotGoalie(random_player)

    context['active_class_id'] = 'player_of_the_day'
    context['header'] = 'Player of the day.'
    return render(request, template_name, context)


def about(request):
    learning = ['Python', 'Git', 'Django', 'Data Bases', 'Twitter Bootstrap', 'JSON', 'Web Services', 'and so forth...']
    context = {'learning': learning,
               'active_class_id': 'about'}
    return render(request, 'about.html', context)


def searchPlayer(request):

    errors = []
    context = {'errors': errors,
               'active_class_id': 'search_player'}

    if 'q' in request.GET:
        search_name = request.GET['q']
        if not search_name:
            errors.append('Enter a search term.')
        elif len(search_name) < 3:
            errors.append('Please enter at least 3 letters.')
        else:
            found_players = HockeyPlayer.objects.filter(full_name__icontains=search_name)

            if not found_players:
                errors.append('No players found.')
                return render(request, 'search_player.html', context)

            found_players = found_players.exclude(team__team_name='NO_TEAM').exclude(position='NO_POSITION')
            # TODO: deside on - eliminate from search results OR somehow mark players without any data to plot.
            context['players'] = found_players
            context['query'] = search_name
            return render(request, 'search_player.html', context)

    return render(request, 'search_player.html', context)


def getContextToPlotPlayer(player):
    player_records = PlayerScores.objects.filter(player=player).filter(Season='2013-2014 REGULAR SEASON')
    if not player_records:
        errors = ['No data available for plotting.']
        template_name = 'search_player.html'
        context = {'errors': errors,
                   'active_class_id': 'search_player'}
        return template_name, context

    goals_data = []
    assists_data = []
    points_data = []
    plus_minus_data = []
    for record in player_records:
        goals_data.append([record.GP, record.G])
        assists_data.append([record.GP, record.A])
        points_data.append([record.GP, record.P])
        plus_minus_data.append([record.GP, record.PlusMinus])

    data_dict = {'goals_data': goals_data,
                 'assists_data': assists_data,
                 'points_data': points_data,
                 'plus_minus_data': plus_minus_data}
    template_name = 'plot_player.html'

    record_count = len(player_records)
    current_record = player_records[record_count-1]

    data_dump = json.dumps(data_dict)
    context = {'player': player,
               'current_record': current_record,
               'data_dump': data_dump}
    return template_name, context


def getContextToPlotGoalie(player):
    player_records = GoalieScores.objects.filter(player=player).filter(Season='2013-2014 REGULAR SEASON')
    if not player_records:
        errors = ['No data available for plotting.']
        template_name = 'search_player.html'
        context = {'errors': errors,
                   'active_class_id': 'search_player'}
        return template_name, context

    goals_against_data = []
    saves_data = []
    save_percentage_data = []
    goals_against_average_data = []
    for record in player_records:
        goals_against_data.append([record.GP, record.GA])
        saves_data.append([record.GP, record.Sv])
        save_percentage_data.append([record.GP, record.SvPercentage])
        goals_against_average_data.append([record.GP, record.GAA])

    data_dict = {'goals_against_data': goals_against_data,
                 'saves_data': saves_data,
                 'save_percentage_data': save_percentage_data,
                 'goals_against_average_data': goals_against_average_data}
    template_name = 'plot_goalie.html'

    record_count = len(player_records)
    current_record = player_records[record_count-1]

    data_dump = json.dumps(data_dict)
    context = {'player': player,
               'current_record': current_record,
               'data_dump': data_dump}
    return template_name, context


def plotAnyPlayer(request, pk):
    player = HockeyPlayer.objects.get(pk=pk)
    position = player.position

    if position != 'Goalie':
        template_name, context = getContextToPlotPlayer(player)
    else:
        template_name, context = getContextToPlotGoalie(player)

    return render(request, template_name, context)
