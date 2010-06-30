.. _introduction

***************
Introduction
***************

The anolis microsatellite primer database is a project we started to use the available *Anolis carolinensis* genomic sequence to design microsatellite DNA primers for Anolis because, strangely, there was not a set of decent primers.

anoCar1 microsatellite primer database [deprecated]
===================================================

Given that we had an entire genome at our disposal, we sort of went overboard - and we *initially* located and designed tagged primers [Schuelke2000, Boutin-Ganache2001]_ for roughly 30,000 microsatellite loci in the Anolis genome.  The code we initially used for the first version the database is available in `downloads <http://github.com/banddna/anolis/downloads>`_ as v0.1 (SHA: 60e9d31)

With the advent of the anoCar2 genome assembly (available at `ftp://ftp.broad.mit.edu/distribution/assemblies/reptiles/lizard/ <ftp://ftp.broad.mit.edu/distribution/assemblies/reptiles/lizard/>`_, we were in a bit of a pickle because we had initially built the database from a semi-hodgepodge of scripts using the anoCar1 genome build.  We had also focused only on certain classes of microsatellite repeats in an effort to save time, rather than designing primers for dinucs, trinucs, tetranucs, pentanucs, and hexanucs.

Because remapping reads from one build to another is generally frustrating, we just decided to begin anew and "start-over" with our Anolis primer database...

anoCar2 microsatellite primer database
=======================================

We built the second version of the anolis microsatellite database during June 26-27, 2010 using a (currently) unreleased version of `msatcommander <http://github.com/brantfaircloth/msatcommander>`_ that is beefed up to deal with genome-scale data.

We scanned a fasta format anoCar2 build constructed from the read and AGP files available at `ftp://ftp.broad.mit.edu/distribution/assemblies/reptiles/lizard/ <ftp://ftp.broad.mit.edu/distribution/assemblies/reptiles/lizard/>`_, searching for mononuc, dinuc, trinuc, tetranuc, pentanuc, and hexanuc repeats of minimum motif lengths 10,6,4,4,4,4; respectively.

We combined complex/compound repeats within <50 bp of one another, and we designed and tagged primers for those repeats where we could, using `primer3 <http://primer3.sourceforge.net>`_, v2, which incorporates thermodynamic parameters to the primer design process - in theory, yielding "better" primers.  We also set the primer3 parameters to consider only multiple candidate primers for a particular locus that were ≥ 10 bp from one another - ensuring that each primer chosen is really unique, to some extent (and more likely to amplify product if another primer should fail).

Because of the volume of the data, and the need for a database that supports concurrent writes, we initially stored the motif and primer data in a MySQL database while we ran the program.  We subsequently copied the table data to a `sqlite <http://www.sqlite.org/>`_ database for distribution.


By the numbers
**************

Motifs
------

- Dinucs      153,558
- Trinucs     389,018
- Tetranucs   100,290
- Pentanucs   5,761
- Hexanucs    2,067


Primers
-------

- 558,618 primers designed (simple/compound/complex loci; up to 4 primers per locus)
- 349,547 primers tagged with M13R or CAG sequences for polymorphism testing
- 115,538 "Best" tagged primers designed where "Best" in this sense means the best of up to 4 primers that may have had tags applied to them.  The criteria for "best" is the primer (of the ≤4) that has the lowest values for the "nasties" (e.g. self-complementarity, pair-complementarity, etc.) that also should allow amplification (e.g. it's within spec.)

Availability
************

At present, we have not posted the primer database while we QC the results a bit and build some supporting files (BED locations of primers, etc.).  However, if you would like a copy of the sqlite dbase, please send an email to:

    faircloth+anolis _at_ gmail _dot_ com