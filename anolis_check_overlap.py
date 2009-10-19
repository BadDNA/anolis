#!/usr/bin/env python
# encoding: utf-8
"""
anolis_check_overlap.py

Created by Brant Faircloth on 2009-10-19.
Copyright (c) 2009 Brant Faircloth. All rights reserved.
"""

import pdb
import os
import sys
import sqlite3
import optparse


def getMainSequenceList(cur):
    cur.execute('''SELECT id, seq_name, seq_start, seq_stop FROM sequence''')
    return cur.fetchall()


def overlapper(conn, cur, seq_list):
    #pdb.set_trace()
    for s in seq_list:
        overlap = 0
        overlap_seq = []
        scaffold = '_'.join(s[1].split('_')[0:2])
        scaffold_q = scaffold + '%'
        seq_id = s[0]
        seq_start, seq_stop = s[2], s[3]
        cur.execute('''SELECT id, seq_name, seq_start, seq_stop FROM sequence WHERE id != ? AND seq_name LIKE ?''', (seq_id, scaffold_q))
        compare_list = cur.fetchall()
        for c in compare_list:
            c_id = c[0]
            c_start, c_stop = c[2], c[3]
            # check to see if seq is within compare range
            if c_start <= seq_start <= c_stop or c_start <= seq_stop <= c_stop:
                overlap = 1
                if c_id not in overlap_seq:
                    overlap_seq.append(c_id)
            # check to see if compare is within seq range            
            if seq_start <= c_start <= seq_stop or seq_start <= c_stop <= seq_stop:
                overlap = 1
                if c_id not in overlap_seq:
                    overlap_seq.append(c_id)
        #pdb.set_trace()
        cur.execute('''UPDATE sequence SET overlap = ? WHERE id = ?''', (overlap, seq_id))
        if overlap_seq:
            for o in overlap_seq:
                cur.execute('''INSERT INTO overlaps (id, overlap_id) VALUES (?,?)''', (seq_id, o))
        conn.commit()


def createTable(cur):
    try:
        # if previous tables exist, drop them
        # TODO: fix createDbase() to drop tables safely
        cur.execute('''drop table overlaps''')
    except:
        pass
    cur.execute('''create table overlaps (
    id int,
    overlap_id int
    )''')

def alterTable(cur):
    try:
        cur.execute('''UPDATE sequence SET OVERLAP = ?''', (None,))
    except:
        cur.execute('''ALTER TABLE sequence ADD COLUMN overlap int''')


def interface():
    '''Command-line interface'''
    usage = "usage: %prog [options]"

    p = optparse.OptionParser(usage)

    p.add_option('--database', '-d', dest = 'database', action='store', \
    type='string', default = None, help='The path to the storage database.', metavar='FILE')

    (options,arg) = p.parse_args()

    if not options.database or not os.path.isfile(options.database):
        print "You must provide a valid path to the database."
        p.print_help()
        sys.exit(2)
        
    return options, arg

def main():
    options, args = interface()
    conn = sqlite3.connect(options.database)
    cur = conn.cursor()
    createTable(cur)
    alterTable(cur)
    seq_list = getMainSequenceList(cur)
    overlapper(conn, cur, seq_list)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()

