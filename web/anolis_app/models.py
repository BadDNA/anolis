#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Column, INTEGER, TEXT, FLOAT, ForeignKey
from anolis_app.database import Base

class Msats(Base):
    __tablename__ = 'msats'
    sequence_id = Column(u'sequence_id', INTEGER(), ForeignKey(u'sequence.id'),\
                            primary_key=True, nullable=False)
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False)
    motif = Column(u'motif', TEXT(length=None, convert_unicode=False,\
                    assert_unicode=None, unicode_error=None, _warn_on_bytestring=False))
    start = Column(u'start', INTEGER())
    end = Column(u'end', INTEGER())
    preceding = Column(u'preceding', INTEGER())
    following = Column(u'following', INTEGER())
    motif_count = Column(u'motif_count', INTEGER())
    
    def __init__(self, sequence_id=None, id=None, motif=None, start=None, \
                end=None, preceding=None, following=None, motif_count=None):
        self.sequence_id = sequence_id
        self.id = id
        self.motif = motif
        self.start = start
        self.end = end
        self.preceding = preceding
        self.following = following
        self.motif_count = motif_count
        
    def __repr__(self):
        return '<Msat %s at %s in %s>' % (self.sequence_id, self.start, self.id)

class Sequence(Base):
    __tablename__ = 'sequence'
    id = Column(u'id', INTEGER(), primary_key=True)
    name = Column(u'name', TEXT(length=None, convert_unicode=False,\
                    assert_unicode=None, unicode_error=None, _warn_on_bytestring=False))

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Sequence %s (%s)>' % (self.name, self.id)

class Combined(Base):
    __tablename__ = 'combined'
    sequence_id = Column(u'sequence_id', INTEGER(), ForeignKey(u'sequence.id'), primary_key=True, nullable=False)
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False)
    motif = Column(u'motif', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                            unicode_error=None, _warn_on_bytestring=False))
    start = Column(u'start', INTEGER())
    end = Column(u'end', INTEGER())
    preceding = Column(u'preceding', INTEGER())
    following = Column(u'following', INTEGER())
    members = Column(u'members', INTEGER())

    def __init__(self, sequence_id=None, id=None, motif=None, start=None,\
                end=None, preceding=None, following=None, members=None):
        self.sequence_id = sequence_id
        self.id = id
        self.motif = motif
        self.start = start
        self.end = end
        self.preceding = preceding
        self.following = following
        self.members = members
        
    def __repr__(self):
        return '<Combined %s>' % (self.id)

class Primers(Base):
    __tablename__ = 'primers2'
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False)
    sequence_id = Column(u'sequence_id', INTEGER(), ForeignKey(u'combined.sequence_id'), nullable=False)
    combined_id = Column(u'combined_id', INTEGER(), ForeignKey(u'combined.id'), nullable=False) 
    primer = Column(u'primer', INTEGER(), nullable=False)
    left_p = Column(u'left_p', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                    unicode_error=None, _warn_on_bytestring=False), nullable=False)
    left_sequence = Column(u'left_sequence', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                            unicode_error=None, _warn_on_bytestring=False), nullable=False)
    left_tm = Column(u'left_tm', FLOAT(precision=None, asdecimal=False))
    left_gc = Column(u'left_gc', FLOAT(precision=None, asdecimal=False))
    left_self_end = Column(u'left_self_end', FLOAT(precision=None, asdecimal=False))
    left_self_any = Column(u'left_self_any', FLOAT(precision=None, asdecimal=False))
    left_hairpin = Column(u'left_hairpin', FLOAT(precision=None, asdecimal=False))
    left_end_stability = Column(u'left_end_stability', FLOAT(precision=None, asdecimal=False))
    left_penalty = Column(u'left_penalty', FLOAT(precision=None, asdecimal=False))
    right_p = Column(u'right_p', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                            unicode_error=None, _warn_on_bytestring=False), nullable=False)
    right_sequence = Column(u'right_sequence', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                            unicode_error=None, _warn_on_bytestring=False), nullable=False)
    right_tm = Column(u'right_tm', FLOAT(precision=None, asdecimal=False))
    right_gc = Column(u'right_gc', FLOAT(precision=None, asdecimal=False))
    right_self_end = Column(u'right_self_end', FLOAT(precision=None, asdecimal=False))
    right_self_any = Column(u'right_self_any', FLOAT(precision=None, asdecimal=False))
    right_hairpin = Column(u'right_hairpin', FLOAT(precision=None, asdecimal=False))
    right_end_stability = Column(u'right_end_stability', FLOAT(precision=None, asdecimal=False))
    right_penalty = Column(u'right_penalty', FLOAT(precision=None, asdecimal=False))
    pair_product_size = Column(u'pair_product_size', FLOAT(precision=None, asdecimal=False))
    pair_compl_end = Column(u'pair_compl_end', FLOAT(precision=None, asdecimal=False))
    pair_compl_any = Column(u'pair_compl_any', FLOAT(precision=None, asdecimal=False))
    pair_penalty = Column(u'pair_penalty', FLOAT(precision=None, asdecimal=False))
    
    def __init__(self, id=None, sequence_id=None, combined_id=None, primer=None, left_p= None, left_sequence=None, left_tm=None, left_gc=None,\
                    left_self_end=None, left_self_any=None, left_hairpin=None, left_end_stability=None, left_penalty=None,\
                    right_p=None, right_sequence=None, right_tm=None, right_gc=None, right_self_end=None, right_self_any=None,\
                    right_hairpin=None, right_end_stability=None, right_penalty=None, pair_compl_end=None, pair_compl_any=None,\
                    pair_penalty=None):
        self.id = id
        self.sequence_id = sequence_id
        self.combined_id = combined_id
        self.primer = primer
        self.left_p = left_p
        self.left_sequence = left_sequence
        self.left_tm = left_tm
        self.left_gc = left_gc
        self.left_self_end = left_self_end
        self.left_self_any = left_self_any
        self.left_hairpin = left_hairpin
        self.left_end_stability = left_end_stability
        self.left_penalty = left_penalty
        self.right_p = right_p
        self.right_sequence = right_sequence
        self.right_tm = right_tm
        self.right_gc = right_gc
        self.right_self_end = right_self_end
        self.right_self_any = right_self_any
        self.right_hairpin = right_hairpin
        self.right_end_stability = right_end_stability
        self.right_penalty = right_penalty
        self.pair_product_size = pair_product_size
        self.pair_compl_end = pair_compl_end
        self.pair_compl_any = pair_compl_any
        self.pair_penalty = pair_penalty
    
    def __repr__(self):
        return '<Primer %s>' % (self.id)

class TaggedPrimers(Base):
    __tablename__ = 'tagged_primers'
    sequence_id = Column(u'sequence_id', INTEGER(), ForeignKey(u'combined.sequence_id'), nullable=False)
    id = Column(u'id', INTEGER(), ForeignKey(u'combined.id'), nullable=False, primary_key=True)
    primer = Column(u'primer', INTEGER(), nullable=False)
    best = Column(u'best', INTEGER(), nullable=False)
    tag = Column(u'tag', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                unicode_error=None, _warn_on_bytestring=False))
    tagged = Column(u'tagged', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                    unicode_error=None, _warn_on_bytestring=False))
    tag_seq = Column(u'tag_seq', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                    unicode_error=None, _warn_on_bytestring=False))
    common = Column(u'common', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                    unicode_error=None, _warn_on_bytestring=False))
    pigtail_tagged = Column(u'pigtail_tagged', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                            unicode_error=None, _warn_on_bytestring=False))
    pigtail_tag_seq = Column(u'pigtail_tag_seq', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                            unicode_error=None, _warn_on_bytestring=False))
    pigtail_common = Column(u'pigtail_common', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                            unicode_error=None, _warn_on_bytestring=False))
    left_p = Column(u'left_p', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                    unicode_error=None, _warn_on_bytestring=False))
    left_sequence = Column(u'left_sequence', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                    unicode_error=None, _warn_on_bytestring=False))
    left_self_end = Column(u'left_self_end', FLOAT(precision=None, asdecimal=False))
    left_self_any = Column(u'left_self_any', FLOAT(precision=None, asdecimal=False))
    left_hairpin = Column(u'left_hairpin', FLOAT(precision=None, asdecimal=False))
    left_penalty = Column(u'left_penalty', FLOAT(precision=None, asdecimal=False))
    right_p = Column(u'right_p', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                    unicode_error=None, _warn_on_bytestring=False))
    right_sequence = Column(u'right_sequence', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                    unicode_error=None, _warn_on_bytestring=False))
    right_self_end = Column(u'right_self_end', FLOAT(precision=None, asdecimal=False))
    right_self_any = Column(u'right_self_any', FLOAT(precision=None, asdecimal=False))
    right_hairpin = Column(u'right_hairpin', FLOAT(precision=None, asdecimal=False))
    right_penalty = Column(u'right_penalty', FLOAT(precision=None, asdecimal=False))
    pair_product_size = Column(u'pair_product_size', FLOAT(precision=None, asdecimal=False))
    pair_compl_end = Column(u'pair_compl_end', FLOAT(precision=None, asdecimal=False))
    pair_compl_any = Column(u'pair_compl_any', FLOAT(precision=None, asdecimal=False))
    pair_penalty = Column(u'pair_penalty', FLOAT(precision=None, asdecimal=False))
    
    def __init__(self, sequence_id, id, primer, best, tag, tagged, tag_seq, common, pigtail_tagged, pigtail_tag_seq, pigtail_common,\
                left_p, left_sequence, left_self_end, left_self_any, left_hairpin, left_penalty, right_p, right_sequence, right_self_end,\
                right_self_any, right_hairpin, right_penalty, pair_product_size, pair_compl_end, pair_compl_any, pair_penalty):
        self.sequence_id = sequence_id
        self.id = id
        self.primer = primer
        self.best = best
        self.tag = tag
        self.tagged = tagged
        self.tag_seq = tag_seq
        self.common = common
        self.pigtail_tagged = pigtail_tagged
        self.pigtail_tag_seq = pigtail_tag_seq
        self.pigtail_common = pigtail_common
        self.left_p = left_p
        self.left_sequence = left_sequence
        self.left_self_end = left_self_end
        self.left_self_any = left_self_any
        self.left_hairpin = left_hairpin
        self.left_penalty = left_penalty
        self.right_p = right_p
        self.right_sequence = right_sequence
        self.right_self_end = right_self_end
        self.right_self_any = right_self_any
        self.right_hairpin = right_hairpin
        self.right_penalty = right_penalty
        self.pair_product_size = pair_product_size
        self.pair_compl_any = pair_compl_any
        self.pair_compl_end = pair_compl_end
        self.pair_penalty = pair_penalty
    
    def __repr__(self):
        return '<TaggedPrimers %s>' % (self.id)

class CombinedComponents(Base):
    __tablename__ = 'combined_components'
    sequence_id = Column(u'sequence_id', INTEGER(), ForeignKey(u'combined.sequence_id'), nullable=False, primary_key=True)
    combined_id = Column(u'combined_id', INTEGER(), ForeignKey(u'combined.id'), nullable=False)
    motif = Column(u'motif', TEXT(length=None, convert_unicode=False, assert_unicode=None,\
                    unicode_error=None, _warn_on_bytestring=False))
    length = Column(u'length', INTEGER(), nullable=False)
    
    def __init__(self, sequence_id, combined_id, motif, length):
        self.sequence_id = sequence_id
        self.combined_id = combined_id
        self.motif = motif
        self.length = length
    
    def __repr__(self):
        return '<CombinedComponents %s:%s>' % (self.sequence_id, self.combined_id)

# def main():
#     from sqlalchemy.orm import sessionmaker
#     from sqlalchemy import create_engine, MetaData, Table
#     from sqlalchemy import create_engine
#     from sqlalchemy.orm import scoped_session, sessionmaker
#     from sqlalchemy.ext.declarative import declarative_base
#     
#     engine = create_engine('sqlite:////Users/nick/Desktop/Code/anolis/web/anolis_app/db/anole2.microsatellites.sqlite', convert_unicode=True)
#     metadata = MetaData()
#     Session = sessionmaker(bind=engine)
# 
# 
# 
#     engine = create_engine('sqlite:////Users/nick/Desktop/Code/anolis/web/db/anole2.microsatellites.sqlite', convert_unicode=True)
#     db_session = scoped_session(sessionmaker(autocommit=False,
#                                              autoflush=False,
#                                              bind=engine))
#     Base = declarative_base()
#     Base.query = db_session.query_property()
#     Base.metadata.create_all(bind=engine)
#     
# 
# if __name__ == '__main__':
#     main()

