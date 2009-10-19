#!/usr/bin/env python
# encoding: utf-8
"""
anolis_bed_formatter.py

Created by Brant Faircloth on 2009-10-19.
Copyright (c) 2009 Brant Faircloth. All rights reserved.
"""

import pdb
import os
import sys
import sqlite3
import optparse


def getMainPrimerList(cur):
    cur.execute('''SELECT sequence.id, sequence.rep_type, sequence.seq_name, 
    primers.l_map, primers.l_strand, primers.r_map, primers.r_strand FROM 
    sequence, primers, tagged 
    WHERE sequence.id = primers.id AND sequence.id = tagged.id and 
    tagged.warning IS NULL AND sequence.overlap = 0 ORDER BY 
    sequence.seq_name''')
    return cur.fetchall()

def formatBedData(output, bd):
    for b in bd:
        #pdb.set_trace()
        l_uc = b[3].split(':')
        scaffold    = l_uc[0]
        # deal with confusing indexing
        l_start     = int(l_uc[1].split('-')[0]) - 1
        l_stop      = l_uc[1].split('-')[1]
        l_strand    = b[4]
        l_name      = str(b[0]) + '_upper'
        # deal with confusing indexing
        r_start     = int(b[5].split(':')[1].split('-')[0]) - 1
        r_stop      = b[5].split(':')[1].split('-')[1]
        r_strand    = b[6]
        r_name      = str(b[0]) + '_lower'
        output.write(('%s %s %s %s 1000 %s %s %s 255,0,0\n') % \
        (scaffold, l_start, l_stop, l_name, l_strand, l_start, l_stop))
        output.write(('%s %s %s %s 1000 %s %s %s 0,0,255\n') % \
        (scaffold, r_start, r_stop, r_name, r_strand, r_start, r_stop))

def interface():
    '''Command-line interface'''
    usage = "usage: %prog [options]"

    p = optparse.OptionParser(usage)

    p.add_option('--output', '-o', dest = 'output', action='store', \
    type='string', default = None, help='''The path to the remasked/output 
    Fasta file.''', metavar='FILE')
    p.add_option('--database', '-d', dest = 'database', action='store', \
    type='string', default = None, help='The path to the storage database.', \
    metavar='FILE')

    (options,arg) = p.parse_args()

    if not options.database or not os.path.isfile(options.database):
        print "You must provide a valid path to the database."
        p.print_help()
        sys.exit(2)
    if os.path.isfile(options.output) or not options.output:
        print '''You must provide a valid path to the output file or ensure
        you are not overwriting another file.'''
        p.print_help()
        sys.exit(2)
        
    return options, arg


def main():
    options, args = interface()
    conn = sqlite3.connect(options.database)
    cur = conn.cursor()
    primerBedData = getMainPrimerList(cur)
    output = open(options.output, 'w')
    output.write('''track name=anolisPrimers description="Tri and Tetranuc Anolis Primers" itemRgb=1 useScore=0\n''')
    formatBedData(output, primerBedData)
    output.close()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()

