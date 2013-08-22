import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import requests


service_address = 'http://127.0.0.1:8000/api'
api_secret = '5e30d905-3aa0-4fe2-973f-e6268135631d'


class Client():
    def __init__(self, service_address, api_secret):
        self.service_address = service_address
        self.api_secret = api_secret

    def addPlayer(self, player_dict):
        player_dict['Secret'] = self.api_secret
        requests.post(self.service_address, data=player_dict)


class ABCTask():
    def __init__(self, url):
        self.url = url

    def processTask(self, context):
        link = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(link.read())
        lastInitials = soup.find('div', {'class': 'lastInitial'})

        tasks = [LetterTask('http://www.nhl.com' + link.get('href') + '&pg=1')
                 for link in lastInitials.find_all('a')]
        context.submitTask(tasks)


class LetterTask():
    def __init__(self, url):
        self.url = url

    def processTask(self, context):
        players_urls = []

        link = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(link.read())

        no_players_on_letter_url = soup.find('div', {'style': 'padding: 6px; font-weight: bold;'}) is not None
        if no_players_on_letter_url:

            tasks = [PlayerTask(players_url) for players_url in players_urls]
            context.submitTask(tasks)

        else:
            node = soup.find('div', {'class': 'resultCount'}).next
            results = node.split()
            result_left_off = int(results[0].split('-')[1])
            result_total = int(results[2])

            for l in soup.find_all('a'):
                candidate = l.get('href')
                candidate = str(candidate)
                if ('http' not in candidate) \
                    and (candidate not in players_urls) \
                    and ('/ice/player.htm?id' in candidate):
                    players_urls.append('http://www.nhl.com' + candidate)

            if result_left_off < result_total:
                next_page = self.url[:self.url.rfind('=') + 1] + str(result_left_off // 50 + 1)

                tasks = [PlayerTask(players_url) for players_url in players_urls]
                context.submitTask(tasks)
                tasks = [LetterTask(next_page)]
                context.submitTask(tasks)

            elif result_left_off == result_total:

                tasks = [PlayerTask(players_url) for players_url in players_urls]
                context.submitTask(tasks)

            else:
                print('something went wrong')


class PlayerTask():
    def __init__(self, url):
        self.url = url

    def processTask(self, context):
        nhl_url = self.url
        try:
            link = urllib.request.urlopen(self.url).read()
        except urllib.error.HTTPError as err:
            # print('ERROR HERE:', self.url)
            return

        soup = BeautifulSoup(link)

        node = soup.find('div', {'style': 'width: 335px;'})
        if node is not None:
            node = node.next
        else:
            node = soup.find('h1', {'style': 'width:550px;'}).next
        full_name = str(node).strip()

        node = soup.find('span', {'class': 'sweater'})
        if node is not None:
            node = node.next
            sweater = str(node)
        else:
            sweater = 'NO_NUMBER'

        node = soup.find('div', {'style': 'float: left; margin-left: 6px; font-weight: bold; color: #999;'})
        if node is not None:
            node = node.next.next
            team = str(node)
        else:
            team = 'NO_TEAM'
            
        node = soup.find('span', {'style': 'color: #666;'}).next
        position = str(node)

        # / TODO find the better way to determine if the current player belongs to any team
        if position == team:
            team = 'NO_TEAM'

        node = soup.find('table', {'class': 'bioInfo'}).next
        birthdate_td_tag = node.contents[-1]
        birthdate_raw_string = birthdate_td_tag.string
        birthdate_raw_list = birthdate_raw_string.split('\n')
        birthdate = birthdate_raw_list[1]

        print('%s - %s - %s - %s - %s' % (full_name, sweater, team, position, birthdate))

        node = soup.find('ul', {'class': 'ui-tabs-nav'})
        node = str(node)

        if 'view=splits' in node:
            url = self.url + '&view=splits'
            try:
                link = urllib.request.urlopen(url).read()
            except urllib.error.HTTPError as err:
                # print('ERROR HERE:', self.url)
                return
            
            soup = BeautifulSoup(link)
            
            if position != 'Goalie':
                node = soup.find('tr', {'class': 'statsRowStyle'})
                stat_values = []
                for _ in range(16):
                    node = node.next.next
                    stat_values.append(node.strip())
                (season, GP, G, A, P, PlusMinus, PIM, PP, SH, GWG, S, Hits,
                 BkS, GvA, TkA, TOIg) = stat_values
                # return [Player.Player(full_name, sweater, team, position,
                #                       season, GP, G, A, P, PlusMinus, PIM, PP,
                #                       SH, GWG, S, Hits, BkS, GvA, TkA, TOIg)]
                player_dict = {'Records available': True,
                               'NHL Url': nhl_url,
                               'Full name': full_name,
                               'Sweater': sweater,
                               'Team': team,
                               'Position': position,
                               'Birthdate': birthdate,
                               'Season': season,
                               'GP': GP,
                               'G': G,
                               'A': A,
                               'P': P,
                               'PlusMinus': PlusMinus,
                               'PIM': PIM,
                               'PP': PP,
                               'SH': SH,
                               'GWG': GWG,
                               'S': S,
                               'Hits': Hits,
                               'BkS': BkS,
                               'GvA': GvA,
                               'TkA': TkA,
                               'TOIg': TOIg}
            else:
                node = soup.find('tr', {'class': 'statsRowStyle'})
                stat_values = []
                for _ in range(7):
                    node = node.next.next
                    stat_values.append(node.strip())
                for _ in range(4):
                    node = node.next.next.next
                    stat_values.append(node)
                node = node.next.next
                stat_values.append(node)
                node = node.next.next.next
                stat_values.append(node)

                (season, GP, GS, W, L, OT, GA, SA, Sv, SvPercentage, GAA, SO,
                 Min) = stat_values
                # return [Goalie.Goalie(full_name, sweater, team, position,
                #                       season, GP, GS, W, L, OT, GA, SA, Sv,
                #                       SvPercentage, GAA, SO, Min)]
                player_dict = {'Records available': True,
                               'NHL Url': nhl_url,
                               'Full name': full_name,
                               'Sweater': sweater,
                               'Team': team,
                               'Position': position,
                               'Birthdate': birthdate,
                               'Season': season,
                               'GP': GP,
                               'GS': GS,
                               'W': W,
                               'L': L,
                               'OT': OT,
                               'GA': GA,
                               'SA': SA,
                               'Sv': Sv,
                               'SvPercentage': SvPercentage,
                               'GAA': GAA,
                               'SO': SO,
                               'Min': Min}
            # TODO *IDEA*: implement addGoalie() and post Players and Goalies to api/Player and api/Goalie respectively.
            # TODO *PURPOSE*: to eliminate some of if-else in countpucks/views.py
        else:
            # player does NOT have SPLITS-page
            # create player
            player_dict = {'Records available': False,
                           'NHL Url': nhl_url,
                           'Full name': full_name,
                           'Sweater': sweater,
                           'Team': team,
                           'Position': position,
                           'Birthdate': birthdate}
        client = Client(service_address, api_secret)
        client.addPlayer(player_dict)
