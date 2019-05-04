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

class DivChoice(Enum):
  DIV_NONE = 1
  DIV_QTY = 2
  DIV_VAL = 3
  

def main(args):
    """ Main entry point of the app """
    print("Process Lots " + __version__)
    print(args)
    
    max_qty = int(args.max_quantity) if args.max_quantity else None
    max_val = float(args.max_value) if args.max_value else None
    min_val = float(args.max_value) if args.max_value else None
    
    bl = blapi.BL()
    
    with open(args.file, newline='') as csvfile:
      reader = csv.DictReader(csvfile)
      with open(args.output_file, 'w', newline='') as outfile:
        fieldnames = reader.fieldnames
        fieldnames.insert(fieldnames.index('Remarks'), 'Used Price')
        fieldnames.insert(fieldnames.index('Remarks'), 'Used Value')
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
          row_qty = int(row['Quantity'])
          row_val = float(row['Value'])
          row_used_price = 0.1 if float(row['Average Price']) == 0.1 else bl.getAveragePrice('PART', row['Part No'], row['Color'])
          row_used_price = float(row_used_price)
          row_used_value = row_qty*row_used_price
          row['Used Price'] = row_used_price
          row['Used Value'] = row_used_value
          div_choice = DivChoice.DIV_NONE
          lot_div = 1
          #print('ID: ' + row['Id'])
          #if (int(row['Id']) == 93):
          #  pdb.set_trace()
          if max_qty is not None and row_qty > max_qty and max_val is not None and row_val > max_val:
            lot_qty_div = math.ceil(row_qty / max_qty)
            lot_val_div = math.ceil(row_val / max_val)
            if lot_qty_div > lot_val_div:
              div_choice = DivChoice.DIV_QTY
              lot_div = lot_qty_div
            else:
              div_choice = DivChoice.DIV_VAL
              lot_div = lot_val_div
          elif max_qty is not None and row_qty > max_qty:
            lot_div = math.ceil(row_qty / max_qty)
            div_choice = DivChoice.DIV_QTY
          elif max_val is not None and float(row['Value']) > max_val:
            lot_div = math.ceil(row_val / max_val)
            div_choice = DivChoice.DIV_VAL

          if (div_choice is not DivChoice.DIV_NONE):
            new_qty = math.floor(row_qty/lot_div)
            row['Quantity'] = new_qty
            row['Value'] = new_qty * float(row['Average Price'])
            row_used_value = new_qty*row_used_price
            row['Used Value'] = row_used_value
            og_id = row['Id']
            for i in range(lot_div):
              row['Id'] = og_id + '.' + str(i+1)
              writer.writerow(row)
          else:
            writer.writerow(row)
          #endif
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