import pprint
import requests
from requests_oauthlib import OAuth1

pp = pprint.PrettyPrinter(indent=2).pprint

base_url = 'https://api.bricklink.com/api/store/v1'

oauth = OAuth1(client_key='0D289F0EE0824820AE7C572DE85ECD57', 
  client_secret='206E19EE065B4DC19BA4ED55072427B6',
  resource_owner_key='BA115784D7C749FF87D782E59EBB288D', 
  resource_owner_secret='9B4904E1C7A34BA4AAF98ED722B82422')

req = requests.get(base_url+'/colors/4', auth=oauth)
res = req.json()
if res['meta']['code'] != 200:
  print('ERROR')
  pp(res['meta'])
else:
  pp(res['data'])

