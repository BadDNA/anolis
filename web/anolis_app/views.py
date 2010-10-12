from anolis_app import app
from flask import Flask, request, flash, redirect, url_for, render_template, jsonify
from flaskext.wtf import Form, TextField, BooleanField, SelectField, SubmitField, IntegerField, validators
# from queries import *
# import models


app.config.update(
    DEBUG=True,
    SECRET_KEY='...'
)


class MyForm(Form):
    size = SelectField(label=u'Msat Size:',\
                        choices=[('mono', 'Mono'),\
                        ('di', 'Di'), ('tri', 'Tri')])
    length = IntegerField(label=u'Msat Length:')
    output = SelectField(label=u'Output Format:',\
                        choices=[('csv','Comma Delimited'),('tab','Tab Delimited')])
    perfect = BooleanField(label=u'Perfect Msats:')
    combine_loci = IntegerField(label=u'Combine Microsatellites:')
    design_primers = BooleanField(label=u'Design Primers:')
    tag_primers = SelectField(label=u'Tag Primers:',\
                                choices=[('cag', 'CAG Tag'),\
                                ('m13', 'M13R Tag')])
    pigtail_primers = BooleanField(label=u'Pigtail Primers')
    submit = SubmitField()

@app.route('/query_result')
def add_numbers():
  	size = request.args.get('size', 0, type=int) 
  	length = request.args.get('length', 0, type=int)
  	combine_loci = request.args.get('combine_loci', False, type=bool)
  	tag_primers = request.args.get('tag_primers', False, type=bool)
  	print 'running query'
	return jsonify(result='Processed Form')



@app.route("/")
def submit():
    form = MyForm(csrf_enabled=True)
    print 'here'
    return render_template("index.html", form=form)