#!/usr/bin/env python3
"""
Create New Draft
"""

__author__ = "Peter Lieber"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import csv
from enum import Enum
import math
import blapi
import pdb
import pprint
  

def main(args):
  """ Main entry point of the app """
  print("Create Draft " + __version__)
  print(args)
  
  pp = pprint.PrettyPrinter(indent=2,width=160).pprint
  
  bl = blapi.BL()
  
  subsets = bl.getSubsets('Set', args.set)
  
  parts = []
  for p in subsets:
    part = p['entries'][0]['item']
    part['color_id'] = p['entries'][0]['color_id']
    part['quantity'] = p['entries'][0]['quantity']
    part['extra_quantity'] = p['entries'][0]['extra_quantity']
    part['value'] = bl.getAveragePrice('Part', part['no'], part['color_id'])
    parts += [part]
  
  pp(parts)
#endmain
        
    


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    #parser.add_argument("file", help="Input Lot CSV File")
    parser.add_argument("set", help="Set Number")
    parser.add_argument("qty", help="Quantity of Sets to draft")

    # Optional argument flag which defaults to False
    #parser.add_argument("-u", "--used", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-mv", "--max_value", action="store", dest="max_value")
    parser.add_argument("-mq", "--max_quantity", action="store", dest="max_quantity")
    parser.add_argument("-o", "--output_file", action="store", dest="output_file", default='lots.csv')

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    
    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)