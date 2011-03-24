from anolis_app.database import db_session
from anolis_app.models import Msats, Sequence, Combined, Primers

def run_query(msat_motif, msat_motif_size, msat_motif_count, combine_loci, design_primers, tag_primers):
	"""Take the args from the webpage and submit to the database
	
		I'm not a big fan of composing the python expression as a string and then evaling
		at the end, but it still beats writing raw SQL.
	"""
	
	
	print msat_motif, msat_motif_size, msat_motif_count, combine_loci, design_primers, tag_primers
	# 		None 				4 			10 F			False 			True 			None
	
	
	results_dict = {"total_msats": 0.0,
				"mean_repeats": 0.0,
				"stdev_repeast": 0.0,
				"dis_count": 0.0,
				"tris_count": 0.0,
				"tetras_count": 0.0,
				"pentas_count": 0.0,
				"hexas_count": 0.0,
				"heptas_count": 0.0,
				"octas_count": 0.0,
				"nonas_count": 0.0,
				}
	
	query = 'db_session.query(Msats)'
	
	# filter on motif
	if msat_motif != 'None':
		query += '.filter(Msats.motif == msat_motif)'
			
	# filter on motif size
	if msat_motif_size > 0:
		query += ".filter('length(motif) == :msat_motif_size').params(msat_motif_size = msat_motif_size)"
		
	# filter on length (motif count)
	if msat_motif_count > 0: # need to determine minimun size in db
		query += '.filter(Msats.motif_count == msat_motif_count)'
		
	# filter on design primers
	if design_primers == True:
		pass
	
	# filter on primers
	
	# filter on tag
	#http://www.sqlalchemy.org/
	# get and return data

	if query != 'db_session.query(Msats)':
		count_rows = query + '.count()'
		row_count = eval(count_rows)
		results_dict['total_msats'] = row_count
		query += '.all()'
		print query
				
# 		for count, row in enumerate(eval(query)):
# 			print row.motif, row.start, row.end, row.motif_count
# 			if count > 10: break
							
		return results_dict
	else:
		return 'No Query'