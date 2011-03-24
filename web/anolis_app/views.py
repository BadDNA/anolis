from anolis_app import app
from flask import Flask, request, flash, redirect, url_for, render_template, jsonify
from flaskext.wtf import Form, TextField, BooleanField, SelectField, SubmitField, IntegerField, validators
from anolis_app.queries import run_query

app.config.update(
    DEBUG=True,
    SECRET_KEY='...'
)


class MyForm(Form):
	# I got the choices with the following query: db_session.query(Msats.motif).distinct().all()
	# Hard coded because the query is slow, but could add a 'unique' table to the db in the furture
	# to remove clutter from this page
	
    msat_motif = SelectField(label=u'Microsatellite Motif Sequence:', \
                        choices=[('None', 'None'), (u'AAAAAC',u'AAAAAC'),(u'AAAAAG', u'AAAAAG'), (u'AAAAAT',  u'AAAAAT'),  (u'AAAAC',   u'AAAAC'),\
                        (u'AAAACC', u'AAAACC'), (u'AAAACT', u'AAAACT'),  (u'AAAAG', u'AAAAG'), (u'AAAAGG', u'AAAAGG'), (u'AAAAT',\
                        u'AAAAT'), (u'AAAATG',  u'AAAATG'), (u'AAAC',  u'AAAC'), (u'AAACAC', u'AAACAC'),  (u'AAACAG', u'AAACAG'),\
                        (u'AAACAT',  u'AAACAT'),  (u'AAACC', u'AAACC'),  (u'AAACT',  u'AAACT'),  (u'AAAG', u'AAAG'),  (u'AAAGAC',\
                        u'AAAGAC'), (u'AAAGAG',  u'AAAGAG'), (u'AAAGC', u'AAAGC'), (u'AAAGCC',  u'AAAGCC'), (u'AAAGG', u'AAAGG'),\
                        (u'AAAGGC', u'AAAGGC'), (u'AAAGGG', u'AAAGGG'), (u'AAAGGT', u'AAAGGT'), (u'AAAGT', u'AAAGT'), (u'AAAGTC',\
                        u'AAAGTC'), (u'AAAT',  u'AAAT'), (u'AAATAC', u'AAATAC'), (u'AAATAG',  u'AAATAG'), (u'AAATAT', u'AAATAT'),\
                        (u'AAATC', u'AAATC'),  (u'AAATCC', u'AAATCC'), (u'AAATCT', u'AAATCT'),  (u'AAATG', u'AAATG'), (u'AAATGT',\
                        u'AAATGT'),  (u'AAATT',  u'AAATT'), (u'AAATTT',  u'AAATTT'),  (u'AAC',  u'AAC'), (u'AACAAG',  u'AACAAG'),\
                        (u'AACAAT', u'AACAAT'),  (u'AACAC', u'AACAC'), (u'AACACC', u'AACACC'),  (u'AACAG', u'AACAG'), (u'AACAGC',\
                        u'AACAGC'), (u'AACAT', u'AACAT'), (u'AACATC', u'AACATC'), (u'AACATG', u'AACATG'), (u'AACATT', u'AACATT'),\
                        (u'AACC', u'AACC'),  (u'AACCAC', u'AACCAC'),  (u'AACCAG', u'AACCAG'), (u'AACCAT',  u'AACCAT'), (u'AACCC',\
                        u'AACCC'), (u'AACCCC', u'AACCCC'), (u'AACCCT',  u'AACCCT'), (u'AACCT', u'AACCT'), (u'AACCTC', u'AACCTC'),\
                        (u'AACCTT',  u'AACCTT'), (u'AACG',  u'AACG'), (u'AACGAC',  u'AACGAC'), (u'AACGG',  u'AACGG'), (u'AACGGG',\
                        u'AACGGG'),  (u'AACT', u'AACT'),  (u'AACTAC', u'AACTAC'),  (u'AACTAT', u'AACTAT'),  (u'AACTC', u'AACTC'),\
                        (u'AACTG',  u'AACTG'), (u'AACTGT',  u'AACTGT'),  (u'AACTT', u'AACTT'),  (u'AACTTG', u'AACTTG'),  (u'AAG',\
                        u'AAG'),  (u'AAGAAT', u'AAGAAT'),  (u'AAGAC',  u'AAGAC'), (u'AAGAG',  u'AAGAG'), (u'AAGAGC',  u'AAGAGC'),\
                        (u'AAGAGG', u'AAGAGG'),  (u'AAGAT', u'AAGAT'), (u'AAGATG', u'AAGATG'),  (u'AAGATT', u'AAGATT'), (u'AAGC',\
                        u'AAGC'), (u'AAGCAC',  u'AAGCAC'), (u'AAGCAG', u'AAGCAG'), (u'AAGCAT',  u'AAGCAT'), (u'AAGCC', u'AAGCC'),\
                        (u'AAGCGG',  u'AAGCGG'), (u'AAGCT',  u'AAGCT'), (u'AAGCTG',  u'AAGCTG'), (u'AAGG',  u'AAGG'), (u'AAGGAG',\
                        u'AAGGAG'), (u'AAGGC',  u'AAGGC'), (u'AAGGCG', u'AAGGCG'), (u'AAGGCT',  u'AAGGCT'), (u'AAGGG', u'AAGGG'),\
                        (u'AAGGGG',  u'AAGGGG'), (u'AAGGT',  u'AAGGT'), (u'AAGGTG',  u'AAGGTG'), (u'AAGT',  u'AAGT'), (u'AAGTAG',\
                        u'AAGTAG'),  (u'AAGTC',  u'AAGTC'),  (u'AAGTG',  u'AAGTG'),  (u'AAGTGT',  u'AAGTGT'),  (u'AAT',  u'AAT'),\
                        (u'AATAC', u'AATAC'),  (u'AATACT', u'AATACT'), (u'AATAG', u'AATAG'),  (u'AATAGC', u'AATAGC'), (u'AATAGT',\
                        u'AATAGT'), (u'AATAT', u'AATAT'), (u'AATATC', u'AATATC'), (u'AATATG', u'AATATG'), (u'AATATT', u'AATATT'),\
                        (u'AATC',  u'AATC'), (u'AATCAC',  u'AATCAC'),  (u'AATCAT', u'AATCAT'),  (u'AATCC', u'AATCC'),  (u'AATCT',\
                        u'AATCT'), (u'AATCTC',  u'AATCTC'), (u'AATG',  u'AATG'), (u'AATGAG', u'AATGAG'),  (u'AATGAT', u'AATGAT'),\
                        (u'AATGC', u'AATGC'),  (u'AATGCT', u'AATGCT'), (u'AATGG', u'AATGG'),  (u'AATGGG', u'AATGGG'), (u'AATGGT',\
                        u'AATGGT'),  (u'AATGT', u'AATGT'),  (u'AATT', u'AATT'),  (u'AATTAG', u'AATTAG'),  (u'AATTAT', u'AATTAT'),\
                        (u'AATTC',  u'AATTC'),  (u'AC',  u'AC'),   (u'ACACAG',  u'ACACAG'),  (u'ACACAT',  u'ACACAT'),  (u'ACACC',\
                        u'ACACC'), (u'ACACCC', u'ACACCC'), (u'ACACGC',  u'ACACGC'), (u'ACACT', u'ACACT'), (u'ACACTC', u'ACACTC'),\
                        (u'ACAG',  u'ACAG'), (u'ACAGAG',  u'ACAGAG'),  (u'ACAGAT', u'ACAGAT'),  (u'ACAGC', u'ACAGC'),  (u'ACAGG',\
                        u'ACAGG'),  (u'ACAGT', u'ACAGT'),  (u'ACAT',  u'ACAT'), (u'ACATAG',  u'ACATAG'), (u'ACATAT',  u'ACATAT'),\
                        (u'ACATC', u'ACATC'),  (u'ACATCT', u'ACATCT'), (u'ACATG', u'ACATG'),  (u'ACATGC', u'ACATGC'), (u'ACATGG',\
                        u'ACATGG'),  (u'ACC',  u'ACC'), (u'ACCACT',  u'ACCACT'),  (u'ACCAG',  u'ACCAG'), (u'ACCAGC',  u'ACCAGC'),\
                        (u'ACCAGG', u'ACCAGG'),  (u'ACCAT', u'ACCAT'), (u'ACCATC', u'ACCATC'),  (u'ACCATG', u'ACCATG'), (u'ACCC',\
                        u'ACCC'),  (u'ACCCC', u'ACCCC'),  (u'ACCCCC', u'ACCCCC'),  (u'ACCCCT', u'ACCCCT'),  (u'ACCCG', u'ACCCG'),\
                        (u'ACCCGT',  u'ACCCGT'),  (u'ACCCT', u'ACCCT'),  (u'ACCCTG',  u'ACCCTG'),  (u'ACCG', u'ACCG'),  (u'ACCT',\
                        u'ACCT'), (u'ACCTAT',  u'ACCTAT'), (u'ACCTC', u'ACCTC'), (u'ACCTCC',  u'ACCTCC'), (u'ACCTCT', u'ACCTCT'),\
                        (u'ACCTG',  u'ACCTG'),  (u'ACCTGC',  u'ACCTGC'),  (u'ACCTGG', u'ACCTGG'),  (u'ACG',  u'ACG'),  (u'ACGAG',\
                        u'ACGAG'),  (u'ACGAGG', u'ACGAGG'),  (u'ACGATG',  u'ACGATG'), (u'ACGC',  u'ACGC'), (u'ACGCC',  u'ACGCC'),\
                        (u'ACGG',  u'ACGG'),  (u'ACGGAG',  u'ACGGAG'),  (u'ACGGC',  u'ACGGC'),  (u'ACGGG',  u'ACGGG'),  (u'ACGT',\
                        u'ACGT'), (u'ACT', u'ACT'), (u'ACTAG', u'ACTAG'), (u'ACTAT', u'ACTAT'), (u'ACTATG', u'ACTATG'), (u'ACTC',\
                        u'ACTC'),  (u'ACTCAT', u'ACTCAT'),  (u'ACTCC', u'ACTCC'),  (u'ACTCCT', u'ACTCCT'),  (u'ACTCT', u'ACTCT'),\
                        (u'ACTCTC', u'ACTCTC'),  (u'ACTG', u'ACTG'),  (u'ACTGAG', u'ACTGAG'), (u'ACTGAT',  u'ACTGAT'), (u'ACTGC',\
                        u'ACTGC'),  (u'ACTGCC',  u'ACTGCC'),  (u'ACTGCT',   u'ACTGCT'),  (u'ACTGG',  u'ACTGG'),  (u'AG',  u'AG'),\
                        (u'AGAGAT', u'AGAGAT'), (u'AGAGC', u'AGAGC'), (u'AGAGCC', u'AGAGCC'), (u'AGAGCG', u'AGAGCG'), (u'AGAGCT',\
                        u'AGAGCT'),  (u'AGAGG', u'AGAGG'),  (u'AGAGGC', u'AGAGGC'),  (u'AGAGGG', u'AGAGGG'),  (u'AGAT', u'AGAT'),\
                        (u'AGATAT',  u'AGATAT'), (u'AGATC',  u'AGATC'),  (u'AGATG', u'AGATG'),  (u'AGATGG', u'AGATGG'),  (u'AGC',\
                        u'AGC'),  (u'AGCAGG',  u'AGCAGG'),  (u'AGCAT',  u'AGCAT'), (u'AGCATC',  u'AGCATC'),  (u'AGCC',  u'AGCC'),\
                        (u'AGCCC', u'AGCCC'), (u'AGCCCC', u'AGCCCC'), (u'AGCCCT', u'AGCCCT'), (u'AGCCGC', u'AGCCGC'), (u'AGCCGG',\
                        u'AGCCGG'),  (u'AGCCT',  u'AGCCT'), (u'AGCCTC',  u'AGCCTC'),  (u'AGCG',  u'AGCG'), (u'AGCGG',  u'AGCGG'),\
                        (u'AGCGGC',  u'AGCGGC'),  (u'AGCTC',  u'AGCTC'),  (u'AGCTCC', u'AGCTCC'),  (u'AGG',  u'AGG'),  (u'AGGAT',\
                        u'AGGAT'),  (u'AGGATG', u'AGGATG'),  (u'AGGC',  u'AGGC'), (u'AGGCC',  u'AGGCC'), (u'AGGCCC',  u'AGGCCC'),\
                        (u'AGGCG',  u'AGGCG'), (u'AGGCGG',  u'AGGCGG'),  (u'AGGG', u'AGGG'),  (u'AGGGAT', u'AGGGAT'),  (u'AGGGC',\
                        u'AGGGC'), (u'AGGGCC', u'AGGGCC'), (u'AGGGCG',  u'AGGGCG'), (u'AGGGG', u'AGGGG'), (u'AGGGGG', u'AGGGGG'),\
                        (u'AT', u'AT'), (u'ATATC',  u'ATATC'), (u'ATATCC', u'ATATCC'), (u'ATC',  u'ATC'), (u'ATCATG', u'ATCATG'),\
                        (u'ATCC',  u'ATCC'),  (u'ATCCC',  u'ATCCC'),  (u'ATCCCC',  u'ATCCCC'),  (u'ATCCG',  u'ATCCG'),  (u'ATCG',\
                        u'ATCG'),  (u'ATCGC',  u'ATCGC'),  (u'ATGC',  u'ATGC'),  (u'ATGCC',  u'ATGCC'),  (u'ATGGCC',  u'ATGGCC'),\
                        (u'CCCCG', u'CCCCG'),  (u'CCCG', u'CCCG'),  (u'CCCGG', u'CCCGG'),  (u'CCG', u'CCG'),  (u'CCGG', u'CCGG'),\
                        (u'CG', u'CG')])

    msat_motif_size = SelectField(label=u'Microsatellite Motif Size:',\
                        choices=[('None', 'None'), (2, 'Di'), (3, 'Tri'), (4, 'Tetra'), 
                        (5, 'Penta'), (6,'Hexa')])
    msat_motif_count  = IntegerField(label=u'Microsatellite Motif Count:')
    output_type = SelectField(label=u'Output Format:',\
                        choices=[('csv','Comma Delimited'),('tab','Tab Delimited')])
    msat_perfect = BooleanField(label=u'Perfect Microsatellites:')
    combine_loci = BooleanField(label=u'Combine Microsatellites:')
    design_primers = BooleanField(label=u'Design Primers:')
    tag_primers = SelectField(label=u'Tag Primers:',\
                                choices=[('None','No Tag'), ('cag', 'CAG Tag'),\
                                ('m13', 'M13R Tag')])
    pigtail_primers = BooleanField(label=u'Pigtail Primers')
    # submit = SubmitField()


@app.route('/query_args')
def add_numbers():
	
	# parse arguements
	msat_motif = request.args.get('msat_motif', None, type=str) 
	msat_motif_size = request.args.get('msat_motif_size', 0, type=int) 
  	msat_motif_count = request.args.get('msat_motif_count', 0, type=int)
  	combine_loci = request.args.get('combine_loci', False, type=bool)
  	design_primers = request.args.get('design_primers', False, type=bool)
  	tag_primers = request.args.get('tag_primers', None, type=str)
  	  	
  	# run query
  	query_results = run_query(msat_motif, msat_motif_size, msat_motif_count, combine_loci, design_primers, tag_primers)
  	  	
	return jsonify(numb_msats = query_results['total_msats'], msat_motif_count=msat_motif_count)


@app.route("/")
def submit():
    form = MyForm(csrf_enabled=True)    
    return render_template("index.html", form=form)
    