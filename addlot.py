#!/usr/bin/env python3
"""
Add Row to lot list file
"""

__author__ = "Peter Lieber"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import blapi
import csv
import pprint
import os

def main(args):
    """ Main entry point of the app """
    print("Add Lot")
    print(args)
    
    pp = pprint.PrettyPrinter(indent=2).pprint
    
    if (False and args.init):
      fields=['Id','Image','Part No', 'Name', 'Color', 'Quantity', 
              'Average Price', 'Value', 'Remarks']
      with open(args.file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    
    id = 23
    
    if os.path.exists("lots.dat"):
      with open ("lots.dat", "r") as datfile:
        data=datfile.readlines()
        if data:
          id = int(data[0])
    
    color = args.color
    image_color = 'White' if args.color.lower().startswith('various') else args.color
    bl = blapi.BL()
    item = bl.getItemInfo('PART', args.part_no)
    price = 0.1 if args.color.lower().startswith('various') or args.name else bl.getAveragePrice('PART', args.part_no, args.color)
    image = bl.getImage('PART', args.part_no, image_color)
    quantity = int(args.qty if int(args.weight) <= 0 else (int(args.weight)-1)/float(item['weight']))
    name = item['name'] if not args.name else args.name
    part_no = args.part_no if not args.name else 'N/A'
    pp(item)
    
    fields=[id+1,
            '=IMAGE("HTTP:{}")'.format(image['thumbnail_url']),
            part_no,
            name,
            color,
            quantity,
            price,
            int(quantity)*float(price),
            args.remarks
            ]
    pp(fields)
    
    #for i in fields: print(i)
    #for i in fields: print(repr(i))
    
    if not args.test:
      with open(args.file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
      
      with open ("lots.dat", "w") as datfile:
        datfile.write(str(id+1))
      

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("part_no", help="Lego Design ID")
    parser.add_argument("qty", help="Quantity in Lot")
    parser.add_argument("color", 
      help="BL Color ID or Name")
      
    # Optional argument flag which defaults to False
    parser.add_argument("-i", "--init", action="store_true", default=False)
    parser.add_argument("-t", "--test", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-n", "--name", action="store", dest="name")
    
    parser.add_argument("-w", "--weight", action="store", dest="weight", default=0,
      help="Weight of item, in grams, to calculate quantity")
    
    parser.add_argument("-f", "--file", action="store", dest="file", default='lots.csv',
      help="CSV File to store lots")
    
    parser.add_argument("-r", "--remarks", action="store", dest="remarks",
      help="Remarks about the lot (condition, color, etc.")
    
    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    #parser.add_argument(
    #    "-v",
    #    "--verbose",
    #    action="count",
    #    default=0,
    #    help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)