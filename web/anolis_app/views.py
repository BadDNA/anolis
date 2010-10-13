from anolis_app import app
from flask import Flask, request, flash, redirect, url_for, render_template, jsonify
from flaskext.wtf import Form, TextField, BooleanField, SelectField, SubmitField, IntegerField, validators
from anolis_app.database import db_session
from anolis_app.models import Sequence


app.config.update(
    DEBUG=True,
    SECRET_KEY='...'
)


class MyForm(Form):
    msat_size = SelectField(label=u'Msat Size:',\
                        choices=[('mono', 'Mono'),\
                        ('di', 'Di'), ('tri', 'Tri')])
    msat_length = IntegerField(label=u'Msat Length:')
    output_type = SelectField(label=u'Output Format:',\
                        choices=[('csv','Comma Delimited'),('tab','Tab Delimited')])
    msat_perfect = BooleanField(label=u'Perfect Msats:')
    combine_loci = BooleanField(label=u'Combine Microsatellites:')
    design_primers = BooleanField(label=u'Design Primers:')
    tag_primers = SelectField(label=u'Tag Primers:',\
                                choices=[('None','No Tag'), ('cag', 'CAG Tag'),\
                                ('m13', 'M13R Tag')])
    pigtail_primers = BooleanField(label=u'Pigtail Primers')
    # submit = SubmitField()

@app.route('/query_result')
def add_numbers():		
	print request.args
	msat_perfect = request.args.get('perfect', False, type=bool)
  	msat_size = request.args.get('msat_size', 'di', type=str) 
  	msat_length = request.args.get('msat_length', 0, type=int)
  	combine_loci = request.args.get('combine_loci', False, type=bool)
  	design_primers = request.args.get('design_primers', False, type=bool)
  	tag_primers = request.args.get('tag_primers', 'None', type=str)
  	
  	print 'perfect', msat_perfect
	print 'msat_size', msat_size
	print 'msat_length', msat_length
	print 'combine_loci', combine_loci
	print 'design_primers', design_primers
	print 'tag_primers', tag_primers
	
	
	
	return jsonify(msat_size=msat_size,msat_length=msat_length)


@app.route("/")
def submit():
    form = MyForm(csrf_enabled=True)    
    return render_template("index.html", form=form)
    