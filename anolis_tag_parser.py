#!/usr/bin/env python
# encoding: utf-8
"""
anolis_notag_parser.py

Created by Brant Faircloth on 2009-10-18.
Copyright (c) 2009 Brant Faircloth. All rights reserved.
"""

import pdb
import os
import re
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

def alterRow(old_row, seq_id, seq_start):
    row = {}
    row['index'] = int(seq_id)
    row['l_primer'] = old_row['l_primer']
    row['r_primer'] = old_row['r_primer']
    row['common_bases'] = 0
    row['tag_seq']      = None
    row['tag_len']      = None
    if row['l_primer'].startswith('GGAAACAG') or row['r_primer'].startswith('GGAAACAG'):
        row['tag'] = 'm13r'
        row['tagged'] = 'left'
    elif row['l_primer'].startswith('CAGTCGGG') or row['r_primer'].startswith('CAGTCGGG'):
        row['tag'] = 'cag'
        row['tagged'] = 'right'
    if old_row['warning'] == '':
        row['warning'] = None
    else:
        row['warning'] = old_row['warning']
    if old_row['comment']:
        # parse out the tag sequence and length
        regex = re.compile('Common Bases Modified,\sTag\s([ACGT]+)')
        matches = re.search(regex, old_row['comment'])
        row['common_bases'] = 1
        row['tag_seq'] = matches.group(1)
        row['tag_len'] = len(row['tag_seq'])
    if not row['common_bases']:
        if row['tag'] == 'cag':
            row['tag_seq'] = 'CAGTCGGGCGTCATCA'
            row['tag_len'] = len(row['tag_seq'])
        elif row['tag'] == 'm13r':
            row['tag_seq'] = 'GGAAACAGCTATGACCAT'
            row['tag_len'] = len(row['tag_seq'])
    return row
    
def createTables(cur):
    try:
        # if previous tables exist, drop them
        # TODO: fix createDbase() to drop tables safely
        cur.execute('''drop table tagged''')
    except:
        pass
    cur.execute('''create table tagged (
    id integer,
    l_primer text,
    r_primer text,
    tag text,
    tagged text,
    common_bases int,
    tag_seq text,
    tag_len int,
    warning text
    )''')
    cur.execute('''create index idx_tagged_id on tagged(id)''')

def insertPrimer(cur, row):
    #pdb.set_trace()
    cur.execute('''INSERT INTO tagged (id, l_primer, r_primer, tag, tagged, 
    common_bases, tag_seq, tag_len, warning) VALUES (:index, :l_primer, \
    :r_primer, :tag, :tagged, :common_bases, :tag_seq, :tag_len, :warning)''', row)
    
def main():
    options, args = interface()
    conn = sqlite3.connect(options.database)
    cur = conn.cursor()
    createTables(cur)
    for row in csv.DictReader(open(options.input), \
    fieldnames = [  'seq_name', 
                    'l_primer', 
                    'l_self_any', 
                    'l_self_end',  
                    'r_primer', 
                    'r_self_any', 
                    'r_self_end', 
                    'pair_compl_any',
                    'pair_compl_end',
                    'warning',
                    'comment'
        ]):
        # skip header row
        if row['seq_name'] == 'Clone':
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

