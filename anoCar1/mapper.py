#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Brant Faircloth and Nicholas Crawford on 2010-01-28.
Copyright (c) 2010 Brant Faircloth. All rights reserved.
"""

import pdb
import sqlite3
import MySQLdb
from utilities import private_data # this is a homemade module that contains my mysql pass
from Bio import SeqFeature
from reportlab.lib  import colors 
from GenomeDiagram import GDDiagram, GDFeatureSet, GDGraphSet, GDTrack


def getRecordsSqlite():
    '''currently this will be by scaffold'''
    conn = sqlite3.connect('anolis.10-19-09.sqlite')
    cur = conn.cursor()
    cur.execute('''select sequence.id, primers.l_start, primers.l_stop from 
        sequence, primers where sequence.id = primers.id and seq_map like 
        "scaffold_0:%"''')
    return cur.fetchall()

def getRecordsMySQL():
    """gets data from appopriate mysql database"""
    password = private_data.mysql_pass() # gets pass from module
    conn = MySQLdb.connect(host = "localhost", user = "nick", passwd = password, db = "anolis_msats")
    cur = conn.cursor()
    cur.execute('''select a.scaffold_id, a.start, a.stop 
            from anocar1 as a, locus as l
            where a.locus_id = l.id and a.scaffold_id = 1 and l.type = 'tetra' ''') 
    return cur.fetchall()

def features(data):
    sequenceFeatureHolder = ()
    for d in data:
        sf = SeqFeature.SeqFeature()
        l = SeqFeature.FeatureLocation(d[1],d[2])
        sf.location = l
        sf.type = 'microsatellite'
        sf.strand = 1
        sequenceFeatureHolder = sequenceFeatureHolder + (sf,)
    return sequenceFeatureHolder

def featureSet(feat, name = 'Microsatellite features'):
    fs = GDFeatureSet(name = name)
    for f in feat:
        fs.add_feature(f)
    return fs

# data = getRecordsSqlite() # get data from Sqlite db
data = getRecordsMySQL()
print "Number of msats", len(data)
feat = features(data)
microsat_features = featureSet(feat)

# create diagram
gdd = GDDiagram('Scaffold_0')
gdt1 = gdd.new_track(1, greytrack=1, name='Microsatellite features', height=0.1, scale_smalltick_interval= 1000000)
print gdt1.to_string
gdfs = gdt1.new_set('feature')

print 'parsing features'
for feature in microsat_features.features.values():
    if feature.type=='microsatellite':
        gdfs.add_feature(feature, colour=colors.red) 

print 'drawing diagram'
# draw the diagram
gdd.draw(format='linear', orientation='landscape', tracklines=0, pagesize='A5', fragments=1, circular=0) 
gdd.write('test.png', 'PNG')


