#!/usr/bin/env python
# encoding: utf-8
"""
anolis_notag_parser.py

Created by Brant Faircloth on 2009-10-18.
Copyright (c) 2009 Brant Faircloth. All rights reserved.
"""

import pdb
import os
import sys
import csv
import sqlite3
import optparse


def interface():
    '''Command-line interface'''
    usage = "usage: %prog [options]"

    p = optparse.OptionParser(usage)

    p.add_option('--input', '-i', dest = 'input', action='store', \
type='string', default = None, help='The path to the input untagged primers file.', \
metavar='FILE')
    p.add_option('--database', '-d', dest = 'database', action='store', \
    type='string', default = None, help='The path to the storage database.', metavar='FILE')

    (options,arg) = p.parse_args()
    if not options.input or not options.database:
        p.print_help()
        sys.exit(2)
    if not os.path.isfile(options.input):
        print "You must provide a valid path to the configuration file."
        p.print_help()
        sys.exit(2)
    return options, arg

def seqLookup(cur, seq_name):
    cur.execute('''select id, seq_start, seq_stop from sequence where seq_name = ?''', (seq_name,))
    return cur.fetchall()[0]

def alterRow(row, seq_id, seq_start):
    row['index'] = int(seq_id)
    scaffold = '_'.join(row['seq_name'].split('_')[0:2])
    l_len = len(row['l_primer'])
    r_len = len(row['r_primer'])
    l_start = seq_start + int(row['l_start'])
    l_stop  = seq_start + int(row['l_start']) + l_len - 1
    row['l_strand'] = '+'
    row['l_start'], row['l_stop'] = l_start, l_stop
    row['l_map'] = ('%s:%s-%s') % (scaffold, l_start, l_stop)
    r_stop = seq_start + int(row['r_start'])
    r_start  = seq_start + int(row['r_start']) - r_len + 1
    row['r_strand'] = '-'
    row['r_start'], row['r_stop'] = r_start, r_stop
    row['r_map'] = ('%s:%s-%s') % (scaffold, r_start, r_stop)
    row['l_tm'] = float(row['l_tm'])
    row['r_tm'] = float(row['r_tm'])
    row['l_gc'] = float(row['l_gc'])
    row['r_gc'] = float(row['r_gc'])
    row['product_size'] = row['r_stop'] - row['l_start']
    return row
    
def createTables(cur):
    try:
        # if previous tables exist, drop them
        # TODO: fix createDbase() to drop tables safely
        cur.execute('''drop table primers''')
    except:
        pass
    cur.execute('''create table primers (
    id integer,
    l_primer text,
    l_tm float,
    l_gc float,
    l_start int,
    l_stop int,
    l_map text,
    l_strand text,
    r_primer text,
    r_tm float,
    r_gc float,
    r_start int,
    r_stop int,
    r_map text,
    r_strand text,
    product_size int
    )''')
    cur.execute('''create index idx_primer_id on primers(id)''')

def insertPrimer(cur, row):
    cur.execute('''INSERT INTO primers (id, l_primer, l_tm, l_gc, l_start, 
    l_stop, l_map, l_strand, r_primer, r_tm, r_gc, r_start, r_stop, r_map, 
    r_strand, product_size) VALUES (:index, :l_primer, :l_tm, :l_gc, \
    :l_start, :l_stop, :l_map, :l_strand, :r_primer, :r_tm, :r_gc, \
    :r_start, :r_stop, :r_map, :r_strand, :product_size)''', row)

def main():
    options, args = interface()
    conn = sqlite3.connect(options.database)
    cur = conn.cursor()
    createTables(cur)
    for row in csv.DictReader(open(options.input), \
    fieldnames = [  'seq_name', 
                    'l_primer', 
                    'l_tm', 
                    'l_gc', 
                    'l_start', 
                    'r_primer', 
                    'r_tm', 
                    'r_gc', 
                    'r_start'
        ]):
        # skip header row
        if row['seq_name'] == 'CLONE':
            pass
        else:
            # get primary id of sequence and start and stop coords
            seq_id, seq_start, seq_stop = seqLookup(cur, row['seq_name'])
            row = alterRow(row, seq_id, seq_start)
            insertPrimer(cur, row)
            conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()

