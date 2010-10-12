from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table
engine = create_engine('sqlite:////Users/nick/Desktop/Code/anolis/web/db/anole2.microsatellites.sqlite', convert_unicode=True)
meta = MetaData()
meta.create_all(bind=engine)

msats = Table('msats', meta, autoload=True, autoload_with=engine)
sequence = Table('sequence', meta, autoload=True, autoload_with=engine)
combined = Table('combined', meta, autoload=True, autoload_with=engine)
primers = Table('primers', meta, autoload=True, autoload_with=engine)
tagged_primers = Table('tagged_primers', meta, autoload=True, autoload_with=engine)
combined_components= Table('combined_components', meta, autoload=True, autoload_with=engine)
