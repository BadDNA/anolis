from flask import Flask, request, flash, redirect, url_for, \
    render_template
from flaskext.wtf import Form, TextField, BooleanField, SelectField, SubmitField, IntegerField, validators

app = Flask(__name__)
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

@app.route("/")
def submit():
    form = MyForm(csrf_enabled=True)
    print form
    if form.validate_on_submit():
        flash("Success")
        redirect(url_for("index"))
    return render_template("index.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)