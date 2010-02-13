#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Nicholas Crawford on 2010-02-13.
Copyright (c) 2010 Boston Univeristy. All rights reserved.
"""

import sys
import os
from utilities import private_data # this is a homemade module that contains my mysql pass
import MySQLdb
import numpy as np
import Image, ImageDraw

def getRecordsMySQL(query):
    """gets data from appopriate mysql database"""
    password = private_data.mysql_pass() # gets pass from module
    conn = MySQLdb.connect(host = "localhost", user = "nick", passwd = password, db = "anolis_msats")
    cur = conn.cursor()
    cur.execute(query) 
    return cur.fetchall()


class DrawChromosome(object):
    """docstring for DrawChromosome"""
    def __init__(self, length_bp, scale, width = 8, side_buffer=200, image_size = (300,1000)):
        super(DrawChromosome, self).__init__()
        self.length_bp = length_bp
        self.scale = scale
        self.width = width
        self.side_buffer = side_buffer
        self.image_size = image_size
        
        # calculate offsets, etc. For internal use
        self.side_buffer=image_size[0]/2
        self.half_chr = width/2
        self.chr_length = 500*scale 
        self.relative_tick_size = self.chr_length / length_bp 

    
    def create_image(self):
        """ initialized image"""
        # in future allow user to set type, make transparent background, and set size here.
        self.im = Image.new("RGB",self.image_size,color='white')
        self.draw = ImageDraw.Draw(self.im) # setup image
    
    def add_chromosome(self):
        """draws chromosome"""
        top_left_chr = (self.side_buffer-self.half_chr, self.side_buffer)
        top_right_chr = (self.side_buffer+self.half_chr, self.side_buffer)
        bottom_right_chr = (self.side_buffer-self.half_chr, self.chr_length+self.side_buffer)
        bottom_left_chr = (self.side_buffer+self.half_chr, self.chr_length+self.side_buffer)
        
        corrds = [top_left_chr, top_right_chr, bottom_left_chr, bottom_right_chr]
        self.draw.polygon(corrds,fill="white", outline="black")
        return corrds 
    
    def add_tick_set(self, ticks, length = 5, color = 'black'):
        """draws ticks"""
        for count, tick in enumerate(ticks):
            tick = int(tick) * self.relative_tick_size
            tick_x_left = self.side_buffer - self.half_chr - length
            tick_x_right = self.side_buffer + self.half_chr + length
            
            corrds = [(tick_x_left, tick+self.side_buffer), (tick_x_right, tick+self.side_buffer)]
            self.draw.line(corrds,fill= color)
        pass
    
    def draw_chromosome(self):
        self.im.show()
          


def main():
    
    # find tetra positions
    tetra_locs = getRecordsMySQL("""select s.name , a.start, a.stop 
            from anocar1 as a, locus as l, scaffold as s
            where l.id = a.locus_id and a.scaffold_id = s.id 
            and s.name = 'scaffold_0' and l.type = 'tetra' """)
    tetra_locs = np.array(tetra_locs)
    tetra_locs = tetra_locs[:,1]
    tetra_locs = tuple(tetra_locs)

    # find primer start positions   
    primer_locs = getRecordsMySQL("""select s.name , a.start, a.stop 
            from anocar1 as a, locus as l, scaffold as s, primers as p
            where l.id = a.locus_id and a.scaffold_id = s.id and l.id = p.locus_id 
            and s.name = 'scaffold_0' and l.type = 'tetra' """)
    primer_locs = np.array(primer_locs)
    primer_locs = primer_locs[:,1]
    primer_locs = tuple(primer_locs)

    # draw chromosome image
    chrm = DrawChromosome(16654889,1.0)    
    chrm.create_image()
    chrm.add_tick_set(tetra_locs,color = 'grey')
    chrm.add_tick_set(primer_locs,color = 'red', length = 8)
    
    chrm.add_chromosome()
    chrm.draw_chromosome()
    pass


if __name__ == '__main__':
    main()

