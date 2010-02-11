#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Brant Faircloth on 2010-01-28.
Copyright (c) 2010 Brant Faircloth. All rights reserved.
"""

import pdb
import sqlite3
from Bio import SeqFeature
from GenomeDiagram import GDDiagram, GDFeatureSet, GDGraphSet, GDTrack


def getRecords(cur):
    '''currently this will be by scaffold'''
    cur.execute('''select sequence.id, primers.l_start, primers.l_stop from 
        sequence, primers where sequence.id = primers.id and seq_map like 
        "scaffold_0:%"''')
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


def main():
    conn = sqlite3.connect('anolis.10-19-09.sqlite')
    cur = conn.cursor()
    data = getRecords(cur)
    feat = features(data)
    # create the feature-set
    microsat_features = featureSet(feat[:20])
    # create track and add feature-set
    gdt1 = GDTrack('Microsatellite features', greytrack=1)
    gdt1.add_set(microsat_features)
    # add tracks to diagram
    gdd = GDDiagram('Scaffold_0')
    pdb.set_trace()
    gdd.add_track(gdd, 2)
    # draw the diagram
    gdd.draw(format='linear', orientation='landscape', tracklines=0, pagesize='A5', fragments=5, circular=0)
    
    pdb.set_trace()


if __name__ == '__main__':
    main()

