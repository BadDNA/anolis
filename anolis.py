#!/usr/bin/env python
# encoding: utf-8
"""
anolis.py

Created by Brant Faircloth on 2009-10-15.
Copyright (c) 2009 Brant Faircloth. All rights reserved.
"""

import pdb
import re
import msat
import numpy
import sqlite3
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import SingleLetterAlphabet

def createMotifInstances(motif, min_length, perfect):
    return msat.seqsearch.MicrosatelliteMotif(motif, min_length, perfect)

def motifCollection(**kwargs):
    possible_motifs = (msat.motif.mononucleotide, msat.motif.dinucleotide, \
    msat.motif.trinucleotide, msat.motif.tetranucleotide,
    msat.motif.pentanucleotide, msat.motif.hexanucleotide)
    # add optional lengths
    possible_motifs = zip(kwargs['min_length'], possible_motifs)
    collection = ()
    if kwargs['scan_type'] == 'all':
        for m in possible_motifs:
            pdb.set_trace()
            collection += (createMotifInstances(m[1], m[0], \
            kwargs['perfect']),)
    elif '+' in kwargs['scan_type']:
        # subtracting 1 so that we get >= options.scan_type
        scan = int(kwargs['scan_type'][0]) - 1
        for m in possible_motifs[scan:]:
            collection += (createMotifInstances(m[1], m[0], \
            kwargs['perfect']),)
    elif '-' in kwargs['scan_type']:
        scan_start = int(kwargs['scan_type'][0]) - 1
        scan_stop = int(kwargs['scan_type'][2])
        for m in possible_motifs[scan_start:scan_stop]:
            collection += (createMotifInstances(m[1], m[0], \
            kwargs['perfect']),)
    else:
        # no iteration here because tuple != nested
        scan = int(kwargs['scan_type'][0]) - 1
        collection += (createMotifInstances(possible_motifs[scan][1], \
        possible_motifs[scan][0], kwargs['perfect']),)
    return collection

def microsatellite(record, msat):
    '''Generalized microsatellite search function'''
    #pdb.set_trace()
    for repeat in range(len(msat.compiled)):
        temp_match = ()
        for m in msat.compiled[repeat].finditer(str(record.seq)):
            temp_match += ((m.span(),m.span()[0],len(record.seq)-m.span()[1]),)
        if temp_match:
            record.matches[msat.motif[repeat]] = temp_match

def msatSearch(record, motifs):
    # add matches attribute to object
    record.matches = {}
    for search in motifs:
        microsatellite(record, search)
    return record

def reMask(record):
    #pdb.set_trace()
    # do some masking tricks
    seq = str(record.seq)
    starts, ends = numpy.array([]), numpy.array([])
    #if record.id == 'scaffold_1621':
    #    pdb.set_trace()
    for motif in record.matches:
        for occurrence in record.matches[motif]:
            pos = occurrence[0]
            start, stop = pos
            #print starts, ends
            if not (starts.any() and ends.any()):
                if len(motif) == 4:
                    r_type = 'tetra'
                elif len(motif) == 3:
                    r_type = 'tri'
                starts = numpy.append(starts,start)
                ends = numpy.append(ends,stop)
                # uppercase msat
                seq = seq[:start] + seq[start:stop].upper() + seq[stop:]
            elif (starts.any() and ends.any()) and (0 in start - ends or 0 in stop - starts):
                if len(motif) == 4:
                    r_type += '+tetra'
                elif len(motif) == 3:
                    r_type += '+tri'
                starts = numpy.append(starts,start)
                ends = numpy.append(ends,stop)
                # uppercase msat
                seq = seq[:start] + seq[start:stop].upper() + seq[stop:]
            else:
                record.skip = True
                break
    # hard-mask non-msat lowercase bases
    regex = re.compile('[acgt]')
    seq = re.sub(regex, 'N', seq)
    # get position of repeat or compound repeat
    # sort starts
    starts.sort()
    begin = starts[0]
    # sort ends
    ends.sort()
    end = ends[-1]
    # update SeqRecord Seq object to our specially-masked version
    record.seq = Seq(seq, SingleLetterAlphabet())
    record.whole_r_type = r_type
    record.whole_begin = int(begin)
    record.whole_end = int(end)
    
def flankDistance(record):
    # count preceding and following _good_ bases of updated 
    # str(seq.record)
    regex = re.compile('[ACGT]+')
    pre_len, pos_len = 0,0
    #pdb.set_trace()
    for match in re.findall(regex, str(record.seq[:record.whole_begin])):
        if len(match) > pre_len:
            pre_len = len(match)
    for match in re.findall(regex, str(record.seq[record.whole_end:])):
        if len(match) > pos_len:
            pos_len = len(match)
    record.pre_len, record.post_len = pre_len, pos_len

def createTables(cur):
    try:
        # if previous tables exist, drop them
        # TODO: fix createDbase() to drop tables safely
        cur.execute('''drop table sequence''')
        cur.execute('''drop table motifs''')
    except:
        pass
    cur.execute('''create table sequence (
    id integer primary key,
    seq_name text,
    seq_map text,
    seq_start int,
    seq_stop int,
    rep_start int,
    rep_stop int,
    rep_type text,
    rep_length int
    )''')
    cur.execute('''create table motifs (
    id integer, 
    motif text,
    start integer,
    stop integer,
    units integer,
    length integer
    )''')
    cur.execute('''create index idx_motifs_id on motifs(id)''')
    cur.execute('''create index idx_sequence_seq_name on sequence(seq_name)''')

def insertData(cur, record, info, seq_index):
    cur.execute('''insert into sequence (id, seq_name, seq_map, seq_start,      
    seq_stop, rep_start, rep_stop, rep_type, 
    rep_length) values (?,?,?,?,?,?,?,?,?)''', (seq_index, record.id, \
    info.map, \
    info.start, info.stop, info.start + record.whole_begin, \
    info.start + record.whole_end - 1, record.whole_r_type, \
    record.whole_end-record.whole_begin))
    
    for motif in record.matches:
        m_len = len(motif)
        #pdb.set_trace()
        for occurrence in record.matches[motif]:
            pos = occurrence[0]
            start, stop = pos
            length = stop - start
            units = length/m_len
            cur.execute('''insert into motifs (id, motif, start, stop, units, 
            length) values (?,?,?,?,?,?)''', (seq_index, motif, \
            info.start + start, info.start + stop - 1, units, length))

class SeqHeader():
    """docstring for ClassName"""
    def __init__(self, header, offset=799):
        sh = header.split('_')
        self.string     = header
        self.scaffold   = '_'.join(sh[0:2])
        self.start      = int(sh[2])-offset
        self.stop       = int(sh[3])+offset+1
        self.motif      = sh[4]
        self.repeat     = sh[5]
        self.length     = float(sh[6])
        self.map        = ('%s:%s-%s') % (self.scaffold, self.start,\
                            self.stop)

def main():
    # create a database
    conn = sqlite3.connect('anolis.sqlite')
    cur = conn.cursor()
    createTables(cur)
    conn.commit()
    # create motifs only once
    motifs = motifCollection(min_length = [10,6,8,8,8,8], scan_type = \
    "4+", perfect = True)
    seq_index = 0
    out_handle = open('test_REMASK.fa', 'w')
    good_records = []
    for record in SeqIO.parse(open('test.fa','rU'), 'fasta'):
        if record.seq:record.skip = False
        # do something with header info
        info = SeqHeader(record.id)
        # find the msat(s)
        msatSearch(record, motifs)
        # we're just gonna cram all of the metrics we need into the sequence
        # record, just because it keeps me from having to pass variables all 
        # over the place.
        if record.matches:
            reMask(record)
        else:
            record.skip = True
        if not record.skip:
            flankDistance(record)
            if record.pre_len >= 25 and record.post_len >= 25:
                insertData(cur, record, info, seq_index)
                conn.commit()
                seq_index += 1
                #pdb.set_trace()
                good_records.append(record)
    SeqIO.write(good_records, out_handle, "fasta")
    out_handle.close()
    cur.close()
    conn.close()
                
                


if __name__ == '__main__':
    main()

