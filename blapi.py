#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import pprint
import requests
from requests_oauthlib import OAuth1
import enum
import csv

ITEMTYPES = ["MINIFIG", "PART", "SET", "BOOK", "GEAR", "CATALOG", "INSTRUCTION", 
  "UNSORTED_LOT", "ORIGINAL_BOX"]


class BL(object):
  def __init__(self):
    self.base_url = 'https://api.bricklink.com/api/store/v1'
    self.oauth = OAuth1(client_key='0D289F0EE0824820AE7C572DE85ECD57', 
      client_secret='206E19EE065B4DC19BA4ED55072427B6',
      resource_owner_key='BA115784D7C749FF87D782E59EBB288D', 
      resource_owner_secret='9B4904E1C7A34BA4AAF98ED722B82422')
    colors = self.getColors()
    self.colormap = {}
    for color in colors:
      self.colormap[color["color_id"]] = color
      self.colormap[color["color_name"]] = color
  
  def getColor(self, id):
    return self.colormap[id]
      
  def getItemInfo(self, type, no):
    req = requests.get(self.base_url+'/items/{type}/{no}'.format(type=type, no=no), auth=self.oauth)
    res = req.json()
    if res['meta']['code'] != 200:
      print('ERROR')
      print(res['meta'])
      return 0
    else:
      return res['data']
      
  def getImage(self, type, no, color='White'):
    req = requests.get(self.base_url+'/items/{type}/{no}/images/{color}'.format(type=type, no=no, color=self.getColor(color)['color_id']), auth=self.oauth)
    res = req.json()
    if res['meta']['code'] != 200:
      print('ERROR')
      print(res['meta'])
      return 0
    else:
      return res['data']
      
  def getPriceGuide(self, type, no, color='White', guide_type='sold', new_or_used='N', verbose=False):
    req = requests.get(self.base_url+'/items/{type}/{no}/price'.format(type=type, no=no), 
      params={
        'color_id': self.getColor(color)['color_id'],
        'guide_type': guide_type,
        'new_or_used': new_or_used
      }, auth=self.oauth)
    res = req.json()
    if res['meta']['code'] != 200:
      print('ERROR')
      print(res['meta'])
      return 0
    else:
      if not verbose: res['data']['price_detail'] = []
      return res['data']
      
  def getSubsets(self, type, no):
    req = requests.get(self.base_url+'/items/{type}/{no}/subsets'.format(type=type, no=no), auth=self.oauth)
    res = req.json()
    if res['meta']['code'] != 200:
      print('ERROR')
      print(res['meta'])
      return 0
    else:
      return res['data']
      
  def getAveragePrice(self, type, no, color):
    pg = self.getPriceGuide(type, no, color)
    if not pg:
      return 0
    else:
      return pg['avg_price']
  
  def getColors(self):
    return self.sendRequest('/colors')
  
  def getOrders(self):
    res = self.sendRequest('/orders', {'direction': 'out'})
    return res
      
  def sendRequest(self, path, params={}):
    req = requests.get(self.base_url+path, params=params, auth=self.oauth)
    res = req.json()
    if res['meta']['code'] != 200:
      print('ERROR')
      print(res['meta'])
    else:
      return res['data']

      
def main(args):
  """ Main entry point of the app """
  print("BL API")
  print(args)
  test()


def test():
  
  pp = pprint.PrettyPrinter(indent=2).pprint

  bl = BL()
  pp(bl.getColor(4))
  print('')
  pp(bl.getColor('Dark Bluish Gray'))
  print('')
  pp(bl.getPriceGuide(type='PART', no='3623', color='Blue'))
  print('')
  print(bl.getAveragePrice(type='PART', no='3623', color='Blue'))

  #pg = bl.getPriceGuide(type='SET', no='41597-1')
  #pp(pg)

  #subset = bl.getSubsets(type='SET', no='41597-1')
  #pp(subset)

  #orders = bl.getOrders()
  #pp(orders)

  #pp(bl.getColors())

  #req = requests.get(base_url+'/colors/4', auth=oauth)
  #res = req.json()
  #if res['meta']['code'] != 200:
  #  print('ERROR')
  #  pp(res['meta'])
  #else:
  #  pp(res['data'])

  
if __name__ == "__main__":
  """ This is executed when run from the command line """
  parser = argparse.ArgumentParser()

  # Required positional argument
  #parser.add_argument("arg", help="Required positional argument")

  # Optional argument flag which defaults to False
  #parser.add_argument("-f", "--flag", action="store_true", default=False)

  # Optional argument which requires a parameter (eg. -d test)
  #parser.add_argument("-n", "--name", action="store", dest="name")

  # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
  parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="Verbosity (-v, -vv, etc)")

  # Specify output of "--version"
  parser.add_argument(
    "--version",
    action="version",
    version="%(prog)s (version {version})".format(version=__version__))

  args = parser.parse_args()
  main(args)
    


