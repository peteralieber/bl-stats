#!/usr/bin/env python3
"""
Process a lot file to split lots based on size and/or value
"""

__author__ = "Peter"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import csv

def main(args):
    """ Main entry point of the app """
    print("Process Lots " + __version__)
    print(args)
    
    max_qty = int(args.max_quantity) if args.max_quantity else None
    max_val = float(args.max_value) if args.max_value else None
    
    with open(args.file, newline='') as csvfile:
      reader = csv.DictReader(csvfile)
      with open(args.output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
          if max_qty is not None and int(row['Quantity']) > max_qty:
            row['Quantity'] = int(row['Quantity'])/2
            og_id = row['Id']
            row['Id'] = og_id + '.1'
            writer.writerow(row)
            row['Id'] = og_id + '.2'
            writer.writerow(row)
          else:
            writer.writerow(row)
        #endfor
      #endwith writer
    #endwith reader
        
    


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("file", help="Input Lot CSV File")

    # Optional argument flag which defaults to False
    #parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-mv", "--max_value", action="store", dest="max_value")
    parser.add_argument("-mq", "--max_quantity", action="store", dest="max_quantity")
    parser.add_argument("-o", "--output_file", action="store", dest="output_file", default='lots_processed.csv')

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    
    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)