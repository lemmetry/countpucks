import requests

# WS address
service_address = 'http://127.0.0.1:8000/api'

# one ring to rule them all
api_secret = '5e30d905-3aa0-4fe2-973f-e6268135631d'

# imaginary data from crawler
data_from_crawler = {'Full name': 'Vasya Zhopkin', 'Sweater': 20, 'Position': 'Left wing', 'Team': 'Cast', 'Secret': api_secret}


response = requests.post(service_address, data_from_crawler)

