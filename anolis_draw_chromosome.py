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

def processSQLoutput(query_result):
    query_result = np.array(query_result)
    query_result = query_result[:,1]
    return tuple(query_result)

class DrawChromosome(object):
    """docstring for DrawChromosome"""
    def __init__(self, length_bp, scale, width = 8, side_buffer=200, image_size = (300,1000)):
        super(DrawChromosome, self).__init__()
        self.length_bp = length_bp
        self.scale = scale
        self.width = width
        self.side_buffer = side_buffer
        self.image_size = image_size
        
        # calculate offsets, etc. For internal class use
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
        
        # draw basic chromosome shape
        top_left_chr = (self.side_buffer-self.half_chr, self.side_buffer)
        top_right_chr = (self.side_buffer+self.half_chr, self.side_buffer)
        bottom_right_chr = (self.side_buffer-self.half_chr, self.chr_length+self.side_buffer)
        bottom_left_chr = (self.side_buffer+self.half_chr, self.chr_length+self.side_buffer)
        
        # note: that something is mixed up with the labels, currently works
        # but should be fixed for clarity. 
        
        left_side = top_left_chr + bottom_right_chr
        right_side = top_right_chr + bottom_left_chr

        self.draw.line(left_side,fill = "black")
        self.draw.line(right_side,fill = "black")
        
        def chromosome_top(self):
            
            chr_length = int(self.chr_length)
            top_left = (self.side_buffer - self.half_chr, self.side_buffer - self.half_chr)
            bottom_right = (self.side_buffer + self.half_chr, self.side_buffer + self.width - self.half_chr)
            
            
            bbox = top_left +  bottom_right
            self.draw.arc(bbox, 180, 0, fill = 'black')
            

        def chromosome_bottom(self):
            chr_length = int(self.chr_length)  # fixes float error
            top_left = (self.side_buffer - self.half_chr, self.side_buffer - self.half_chr + chr_length)
            bottom_right = (self.side_buffer + self.half_chr, self.side_buffer + self.width - self.half_chr + chr_length)
            
            bbox = top_left +  bottom_right
            self.draw.arc(bbox, 0, 180, fill = 'black')
        
        # draw curved top and bottom
        chromosome_top(self)
        chromosome_bottom(self)
    
    def add_tick_set(self, ticks, length = 5, color = 'black'):
        """draws ticks"""
        for count, tick in enumerate(ticks):
            tick = int(tick) * self.relative_tick_size
            tick_x_left = self.side_buffer - self.half_chr - length
            tick_x_right = self.side_buffer + self.half_chr + length
            
            corrds = [(tick_x_left, tick+self.side_buffer), (tick_x_right, tick+self.side_buffer)]
            if count > 10:
                print corrds
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
    tetra_locs = processSQLoutput(tetra_locs)
    
    # find primer start positions   
    primer_locs = getRecordsMySQL("""select s.name , a.start, a.stop 
            from anocar1 as a, locus as l, scaffold as s, primers as p
            where l.id = a.locus_id and a.scaffold_id = s.id and l.id = p.locus_id 
            and s.name = 'scaffold_0' and l.type = 'tetra' """)
    primer_locs = processSQLoutput(primer_locs)

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

