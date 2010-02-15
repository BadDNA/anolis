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
    def __init__(self, length_bp, scale, width = 20, side_buffer=200, image_size = (300,1000)):
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
        
        # note: that something is mixed up with the label.  Althought it currently works
        # the labels should be fixed for clarity. 
        
        left_side = top_left_chr + bottom_right_chr
        right_side = top_right_chr + bottom_left_chr
        white_center = (top_left_chr,top_right_chr,bottom_left_chr,bottom_right_chr)
        
        # draw left and rigth sides of chromosome
        self.draw.polygon(white_center,fill = "white")
        self.draw.line(left_side,fill = "black")
        self.draw.line(right_side,fill = "black")
        
        def chromosome_top(self):
            """draws curve at top of chromosome"""
            
            chr_length = int(self.chr_length)
            top_left = (self.side_buffer - self.half_chr, self.side_buffer - self.half_chr)
            bottom_right = (self.side_buffer + self.half_chr, self.side_buffer + self.width - self.half_chr)
            
            bbox = top_left +  bottom_right
            self.draw.arc(bbox, 180, 0, fill = 'black')
            

        def chromosome_bottom(self):
            """draws curve at bottom of chromosom"""
            chr_length = int(self.chr_length)  # fixes float error
            top_left = (self.side_buffer - self.half_chr, self.side_buffer - self.half_chr + chr_length)
            bottom_right = (self.side_buffer + self.half_chr, self.side_buffer + self.width - self.half_chr + chr_length)
            
            bbox = top_left +  bottom_right
            self.draw.arc(bbox, 0, 180, fill = 'black')
        
        # draw curved top and bottom
        chromosome_top(self)
        chromosome_bottom(self)
    
    def add_tick_set(self, ticks, length = 5, color = 'black', labeled = False, text_color = 'grey'):
        """draws ticks"""
        for count, tick in enumerate(ticks):
            scaled_tick = int(tick) * self.relative_tick_size
            tick_x_left = self.side_buffer - self.half_chr - length
            tick_x_right = self.side_buffer + self.half_chr + length
            tick_y = scaled_tick+self.side_buffer
            
            corrds = [(tick_x_left, tick_y), (tick_x_right, tick_y)]
            self.draw.line(corrds,fill= color)
            
            if labeled == True:
                self.draw.text((tick_x_right, tick_y), str(tick) ,fill=text_color,font=None)
                #.text(y,message,fill=None,font=None)
 
    def add_bp_ticks(self,inc_bp = 1000000, color = 'grey', labeled = True):
        """adds labeled ticks at a specified number of basepairs"""
        if labeled == True:
            ticks =  range(0,self.length_bp,inc_bp)
            self.add_tick_set(ticks,length = 15, labeled = True, text_color = 'grey')
        
        if labeled == False:
            ticks =  range(0,self.length_bp,inc_bp)
            self.add_tick_set(ticks,length = 15, labeled = False)
        
    def show_chromosome(self):
        """writes final image to file"""
        self.im.show()
    
    def save_chromosome(self, name, format = "PNG"):
        self.im.save(name,format)
    
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
    chrm.add_bp_ticks()
    chrm.add_chromosome()
    #chrm.show_chromosome()
    chrm.save_chromosome('test.ps','EPS')
    pass


if __name__ == '__main__':
    main()

