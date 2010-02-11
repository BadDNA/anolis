#!/usr/bin/env python
# encoding: utf-8
"""
createGFF.py

Created by Nicholas Crawford on 2010-02-10.
Copyright (c) 2010 Boston Univeristy. All rights reserved.
"""

import sys
import os
import MySQLdb

"""
get row(s) from db
print data in GFF format

col 1 = seqid (e.g., chr1)
col 2 = anoCar_msat_dbase
col 3 = microsatellite or (SO:0000289)
col 4 = start
col 5 = end
col 7 = . (strand, possibly +)
col 8 = .
col 9 = attributes

attributes = tags

ID = ID from locus table
Name = motif from locus table
Alias = type
"""

def get_lines_from_db():
	"""docstring for get_lines_from_db"""
	conn = MySQLdb.connect(host = "localhost", user = "nick", passwd = "", db = "anolis_msats")
	cursor = conn.cursor()
	
	query = """select a.scaffold_id, a.start, a.stop, l.id, l.motif, l.type 
	from locus as l, anocar1 as a
	where l.id = a.locus_id
	limit 10"""
	
	cursor.execute(query)
	
	print "##gff-version 3"
	for count, line in enumerate(cursor):
		print "scafold_%s\tanoCar_msat_dbase\tSO:0000289\t%s\t%s\t.\t.\tID=%s;Name=%s;Alias=%s" % line
	pass








def main():
	get_lines_from_db()
	pass


if __name__ == '__main__':
	main()

