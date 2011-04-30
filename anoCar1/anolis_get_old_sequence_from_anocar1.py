#!/usr/bin/env python
# encoding: utf-8
"""
get_old_sequence_from_anoCar1.py

Created by Brant Faircloth on April 18, 2011.
Copyright (c) 2011 Brant C. Faircloth. All rights reserved.

"""

import os
import sys
import bx.seq.twobit
from openpyxl.reader.excel import load_workbook

import pdb

def is_a_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def get_random_loci(workbook, sheet):
    wb = load_workbook(workbook)
    ws = wb.get_sheet_by_name(sheet)
    coords = []
    for k,v in enumerate(ws.rows):
        #pdb.set_trace()
        if k == 0:
            pass
        elif not is_a_number(v[0].value):
            pass
        else:
            iden, left, right = v[0].value, v[7].value, v[10].value
            coords.append([left,right, iden])
    return coords

def get_extent_from_coords(rows):
    coords = {}
    for position in rows:
        left = position[0]
        right = position[1]
        iden = position[2]
        scaffold = left.split(":")[0]
        numbers = left.split(":")[1].split('-')
        numbers.extend(right.split(":")[1].split('-'))
        mn = min(numbers)
        mx = max(numbers)
        slc = "{0}:{1}-{2}".format(scaffold, mn, mx)
        coords[iden] = slc
    return coords

def get_reads_from_twobit(coords, twobit_file):
    twobit = bx.seq.twobit.TwoBitFile(file(twobit_file))
    for iden, position in coords.iteritems():
        chromo, bps = position.split(":")
        left, right = bps.split('-')
        seq = twobit[chromo][int(left):int(right)]
        print ">{0}~{1}~{2}\n{3}".format(position, iden, len(seq), seq)
        #pdb.set_trace()
    
def main():
    rows = get_random_loci('/Users/bcf/Git/brant/anolis/data/anolis_random_primers.cag.10-22-2009.xlsx', "Sheet1")
    coords = get_extent_from_coords(rows)
    sequence = get_reads_from_twobit(coords, '/Volumes/Data/Genomes/anoCar/official/anoCar1.2bit')

if __name__ == '__main__':
    main()


