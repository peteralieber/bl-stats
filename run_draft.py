#!/usr/bin/env python3
"""
Process a lot file to split lots based on size and/or value
"""

__author__ = "Peter"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import csv
from enum import Enum
import math
import blapi
import pdb
import pprint
import random

def insert_lot_priority(list, item):
  for i in range(len(list)):
    if list[i][0] > item[0]:
      list = list[:i] + [item] + list[i:]
      return list
  
  list = list + [item]
  return list

def main(args):
    """ Main entry point of the app """
    print("Run Draft " + __version__)
    print(args)
    pp = pprint.PrettyPrinter(indent=2).pprint
    
    bl = blapi.BL()
    lots_taken = {}
    participants = {}
    rows = {}
    
    with open(args.file, newline='') as csvfile:
      reader = csv.DictReader(csvfile)
      fieldnames = reader.fieldnames
      pp(fieldnames)
      participants = {p:[] for p in fieldnames[11:]}
      pp(participants)
      for row in reader:
        rows[row['Id']] = row
        lots_taken[row['Id']] = False
        #pdb.set_trace()
        for participant in participants.keys():
          if row[participant].strip() == "":
            row[participant] = "1000"
          participants[participant] = insert_lot_priority(participants[participant], (int(row[participant]),row['Id']))
        #endfor
      #endfor
    #endwith reader
    for participant in participants:
      pp(participant)
      pp(participants[participant])
      print("")
    #Run Draft
    
    plist = ['Peter Lieber', 'Peter Lieber', 'Peter Lieber', 'Peter Lieber',
              'Alex Midina', 'Alex Midina', 'Alex Midina',
              'Donna Scott', 'Donna Scott',
              'Bobby Edge', 'Bobby Edge',
              'Tim Hutchings', 'Tim Hutchings',
              'Patrick Frain', 'Patrick Frain',
              'Matt Rhody', 'Matt Rhody',
              'Steve Laughlin', 'Steve Laughlin']
    random.shuffle(plist)
    hauls = {p:[] for p in participants.keys()}
    
    
    #participants: lists of priorities
    #plist: turn order
    #hauls: what each participant got
    #turntaken: whether a turn was taken
    turntaken = True
    
    while turntaken:
      turntaken = False
      for p in plist:
        print("Turn: " + p)
        # find first non-taken lot
        if len(participants[p]) > 0:
          while lots_taken[participants[p][0][1]]:
            if len(participants[p]) == 1:
              participants[p] = []
              break
            participants[p] = participants[p][1:]
          #endwhile
          if len(participants[p]) > 0:
            lots_taken[participants[p][0][1]] = True
            hauls[p] = hauls[p] + [participants[p][0]]
            turntaken = True
        #endif
        
      for p in reversed(plist):
        print("Turn: " + p)
        # find first non-taken lot
        if len(participants[p]) > 0:
          while lots_taken[participants[p][0][1]]:
            if len(participants[p]) == 1:
              participants[p] = []
              break
            participants[p] = participants[p][1:]
          #endwhile
          if len(participants[p]) > 0:
            lots_taken[participants[p][0][1]] = True
            hauls[p] = hauls[p] + [participants[p][0]]
            turntaken = True
        #endif
      #endfor
    #endwhile
    
    pp(hauls)
  #endmain

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("file", help="Input Lot CSV File")

    # Optional argument flag which defaults to False
    #parser.add_argument("-u", "--used", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    #parser.add_argument("-mv", "--max_value", action="store", dest="max_value")
    #parser.add_argument("-mq", "--max_quantity", action="store", dest="max_quantity")
    #parser.add_argument("-o", "--output_file", action="store", dest="output_file", default='lots_processed.csv')

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    
    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)