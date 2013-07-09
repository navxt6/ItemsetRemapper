#!/usr/bin/env python
#
#    Copyright 2013 Luigi Grimaudo (grimaudo.luigi@gmail.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import logging
import subprocess
import operator
import math
import sys
import os

import CreateRemapMaps
import RemapFile
import MakeUniqueItemForRow

"""
    Main module
"""
def getItemsetAlgo(type):
    return {
        'itemset': '../bin/fim_all',
        'closed': '../bin/fim_closed',
        'maximal': '../bin/mafia'
    }[type]


def mineItemset(input, type, _support, ordering):
    
    
    #subprocess.call(['java', '-jar', '../bin/spmf.jar', 'run', getItemsetAlgo(type), input, output, support])
    fin = open(input)
    dataset = fin.readlines()
    support = str(math.ceil(float(_support)*len(dataset)))
    logging.info("Support count: " + str(support))
    fin.close()
    
    CreateRemapMaps.createMaps(input, "../data/tmp/w2i", "../data/tmp/i2w", " ")
    RemapFile.remap(" ", input, os.path.splitext(input)[0]+"_int.txt", "../data/tmp/w2i", False)
    MakeUniqueItemForRow.deleteDuplicate(" ", os.path.splitext(input)[0]+"_int.txt", os.path.splitext(input)[0]+"_int_unique.txt")
    if type == "maximal":
        subprocess.call([getItemsetAlgo(type), "-mfi", _support, "-ascii", os.path.splitext(input)[0]+"_int_unique.txt", os.path.splitext(input)[0]+"_int_i.txt"])
    else:
        subprocess.call([getItemsetAlgo(type), os.path.splitext(input)[0]+"_int_unique.txt", support, os.path.splitext(input)[0]+"_int_i.txt"])
    RemapFile.remap(" ", os.path.splitext(input)[0]+"_int_i.txt", os.path.splitext(input)[0]+"_w_i.txt", "../data/tmp/i2w", True)
    fin = open(os.path.splitext(input)[0]+"_w_i.txt")
    dataset = fin.readlines()
    fin.close()
    itemsets = {}
    for itemset in dataset:
        itemset, support = itemset.split("(")
        support = int(support.replace(")", "").strip())
        itemset = itemset.strip()
        itemsets[itemset] = support
    
    sortedItemsets = None
    if ordering == "support":
        sortedItemsets = sorted(itemsets.iteritems(), key=operator.itemgetter(1), reverse=True)
    else:
        
    fout = open(os.path.splitext(input)[0]+"_w_" + type + ".txt", "w")
    fout2 = open(os.path.splitext(input)[0]+"_w_" + type + "k3.txt", "w")
    for itemset in sortedItemsets:
        fout.write(itemset[0] + " " + str(itemset[1]) + "\n")
        if len(itemset[0].split(" "))>2:
            fout2.write(itemset[0] + " " + str(itemset[1]) + "\n")
    fout.close()
    fout2.close()    
        
        
def main():
    # Main parser
    parser = argparse.ArgumentParser(description="Main Module")
    parser.add_argument('-i',   help="Input file path")
    #parser.add_argument('-o',   help="Output file")
    parser.add_argument('-t',   help="Type of itemset to mine")
    parser.add_argument('-s',   help="Support Threshold")
    parser.add_argument('-o',   help="Ordering type")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    
    #mineItemset(args.i, args.o, args.t, args.s)
    mineItemset(args.i, args.t, args.s, args.o)
    
if __name__ == "__main__":
    sys.exit(main())