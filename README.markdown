# Anolis Microsatellite Primer/Locus Website *v1.0* #
A web app for *future* online access to the **Anolis Microsatellite DB**.  It is currently non-functional, but running ('python manage.py') with Flask properly [configured](http://flask.pocoo.org/docs/installation/#installation) will produce a basic webpage with an example form layout.  

The backend is written in [Flask](http://flask.pocoo.org/). The forms are created with using the flask extension of [WTFforms](http://flask.pocoo.org/docs/patterns/wtforms/).  The CSS is from the [blueprintcss framework.] 
(http://www.blueprintcss.org). Javascipt will use the [jquery](jquery.com) library.

# Anolis Microsatellite Primer Database #

The anolis microsatellite primer database is a project we started to use the available _Anolis carolinensis_ genomic sequence to design microsatellite DNA primers for Anolis because, strangely, there was not a set of decent primers.

## anoCar1 microsatellite primer database ##

Given that we had an entire genome at our disposal, we sort of went overboard - and we initially located and designed tagged primers (Schuelke 2000, Boutin-Ganache et al. 2001) for several thousand microsatellite loci in the Anolis genome.  The code we initially used for the first version the database is available in [anolis/downloads](downloads) as v0.1 SHA:  60e9d311fbacf9c2fa2380c7acfd0c4c36b13e29

With the advent of the anoCar2 genome assembly (available at [ftp://ftp.broad.mit.edu/distribution/assemblies/reptiles/lizard/](ftp://ftp.broad.mit.edu/distribution/assemblies/reptiles/lizard/)), we were in a bit of a pickle because we had initially built the database from a semi-hodgepodge of scripts and using the anoCar1 genome build.  We had focused only on certain classes of microsatellite repeats, rather than designing primers for dinucs, trinucs, tetranucs, pentanucs, and hexanucs.

Because remapping reads from one build to another is generally frustrating, we just decided to begin anew and "start-over" with our Anolis primer database.

## anoCar2 microsatellite primer database ##

We built the second version of the anolis microsatellite database during June 26-27, 2010 using a (currently) unreleased version of [msatcommander](http://github.com/brantfaircloth/msatcommander) that is generally scaled up to deal with genome-scale data.

We scanned anoCar2 in fasta format that we built from the read and AGP files available at [ftp://ftp.broad.mit.edu/distribution/assemblies/reptiles/lizard/](ftp://ftp.broad.mit.edu/distribution/assemblies/reptiles/lizard/), searching for mononuc, dinuc, trinuc, tetranuc, pentanuc, and hexanuc repeats of minimum motif lengths 10,6,4,4,4,4, respectively.

We combined complex/compound repeats within <50 bp of one another and then designed and tagged primers for those repeats where we could, using primer3, v2, which incorporates thermodynamics to primer design - which, in theory, should yield "better" primers.

Because of the volume of the data, and the need for a database that supports concurrent writes, we initially stored the motif and primer data in a MySQL database while we ran the program.  We subsequently copied the table data to a [sqlite](http://www.sqlite.org/) database for distribution.

## By the numbers ##

Motifs

* Dinucs      153,558
* Trinucs     389,018
* Tetranucs   100,290
* Pentanucs   5,761
* Hexanucs    2,067

Primers

* 558,618 primers designed (simple/compound/complex loci; up to 4 primers per locus)
* 349,547 primers tagged with M13R or CAG sequences for polymorphism testing
* 115,538 "Best" tagged primers designed where "Best" in this sense means the best of up to 4 primers that may have had tags applied to them.  The criteria for "best" is the primer (of the ≤4) that has the lowest values for the "nasties" (e.g. self-complementarity, pair-complementarity, etc.) that also should allow amplification (e.g. it's within spec.)

## Availability ##

At present, we have not posted the primer database while we QC the results a bit and build some supporting files (BED locations of primers, etc.).  However, if you would like a copy of the sqlite dbase, please send an email to:

    faircloth+anolis _at_ gmail _dot_ com

## License

We provide software on this site under the terms of the BSD License (see LICENSE.txt).  Contents of this site, the accompanying [website](http://baddna.github.com/anolis/), and the primer database are available under a [Creative Commons Attribution 3.0 License](http://creativecommons.org/licenses/by/3.0/), although we may consider alternatives for the distribution of the database.