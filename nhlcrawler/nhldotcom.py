from bs4 import BeautifulSoup
import requests
import json
import socket


if socket.gethostname() == 'vm-VirtualBox':
    service_address = 'http://127.0.0.1:8000/api/'
else:
    service_address = 'http://www.countpucks.com/api/'
api_secret = '947e72de-b090-4979-83a8-fad44b4be3f5'


class Client():
    def __init__(self, service_address, api_secret):
        self.service_address = service_address
        self.api_secret = api_secret

    def addPlayer(self, player_dict):
        player_dict['Secret'] = self.api_secret
        data = json.dumps(player_dict)
        headers = {'content-type': 'application/json'}
        requests.post(self.service_address, data=data, headers=headers)


class ABCTask():
    def __init__(self, url):
        self.url = url

    def processTask(self, context):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text)

        lastInitials = soup.find('div', {'class': 'lastInitial'})

        tasks = [LetterTask('http://www.nhl.com' + link.get('href') + '&pg=1')
                 for link in lastInitials.find_all('a')]
        context.submitTask(tasks)


class LetterTask():
    def __init__(self, url):
        self.url = url

    def processTask(self, context):
        players_urls = []

        response = requests.get(self.url)
        soup = BeautifulSoup(response.text)

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

    def getFullName(self, soup):
        node = soup.find('div', {'style': 'width: 335px;'})
        if node is not None:
            node = node.next
        else:
            node = soup.find('h1', {'style': 'width:550px;'}).next
        full_name = str(node).strip()
        return full_name

    def getSweater(self, soup):
        node = soup.find('span', {'class': 'sweater'})
        if node is not None:
            node = node.next
            sweater = str(node)
        else:
            sweater = 'NO_NUMBER'
        return sweater

    def getTeam(self, soup):
        node = soup.find('div', {'style': 'float: left; margin-left: 6px; font-weight: bold; color: #999;'})
        if node is not None:
            node = node.next.next
            team = str(node)
        else:
            team = 'NO_TEAM'
        return team

    def getPosition(self, soup):
        node = soup.find('span', {'style': 'color: #666;'})
        if node.string is not None:
            node = node.next
            position = str(node)
        else:
            position = 'NO_POSITION'
        return position

    def getBirthdate(self, soup):
        node = soup.find('table', {'class': 'bioInfo'}).next
        birthdate_td_tag = node.contents[-1]
        birthdate_raw_string = birthdate_td_tag.string
        birthdate_raw_list = birthdate_raw_string.split('\n')
        birthdate = birthdate_raw_list[1]
        return birthdate

    def processTask(self, context):
        nhl_url = self.url

        response = requests.get(self.url)
        soup = BeautifulSoup(response.text)

        full_name = self.getFullName(soup)
        sweater = self.getSweater(soup)
        team = self.getTeam(soup)
        position = self.getPosition(soup)

        # / TODO find the better way to determine if the current player belongs to any team
        if position == team:
            team = 'NO_TEAM'

        birthdate = self.getBirthdate(soup)

        print('%s - %s, %s' % (full_name, sweater, team))

        node = soup.find('ul', {'class': 'ui-tabs-nav'})
        node = str(node)

        stat_names = ['Records available', 'NHL Url', 'Full name', 'Sweater', 'Team', 'Position', 'Birthdate']

        player_has_stat_page = 'view=splits' in node
        if player_has_stat_page:
            url = self.url + '&view=splits'

            response = requests.get(url)
            soup = BeautifulSoup(response.text)

            node = soup.find('tr', {'class': 'statsRowStyle'})

            stat_values = [True, nhl_url, full_name, sweater, team, position, birthdate]
            if position != 'Goalie':
                stat_names.extend(['Season', 'GP', 'G', 'A', 'P', 'PlusMinus', 'PIM', 'PP', 'SH', 'GWG', 'S', 'Hits',
                                   'BkS', 'GvA', 'TkA', 'TOIg'])

                for _ in range(16):
                    node = node.next.next
                    stat_values.append(node.strip())
            else:
                stat_names.extend(['Season', 'GP', 'GS', 'W', 'L', 'OT', 'GA', 'SA', 'Sv', 'SvPercentage', 'GAA', 'SO', 'Min'])
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
        else:
            stat_values = [False, nhl_url, full_name, sweater, team, position, birthdate]
        player_dict = dict(zip(stat_names, stat_values))
        client = Client(service_address, api_secret)
        client.addPlayer(player_dict)