CREATE TABLE sequence (id integer, name text, 
	primary key (id));

CREATE TABLE msats (sequence_id integer NOT NULL,
	id integer NOT NULL,
	motif text,
	start integer,
	end integer,
	preceding integer,
	following integer, 
	motif_count integer,
	PRIMARY KEY (sequence_id,id),
	FOREIGN KEY (sequence_id) REFERENCES sequence (id));




CREATE TABLE combined (sequence_id integer NOT NULL,id integer NOT NULL, motif text,start integer,end integer,preceding integer,following integer,members integer,PRIMARY KEY (sequence_id,id),
FOREIGN KEY (sequence_id) REFERENCES sequence (id));

CREATE TABLE combined_components (sequence_id integer NOT NULL,combined_id integer NOT NULL,motif text,length integer NOT NULL,
	
FOREIGN KEY (sequence_id, combined_id) REFERENCES combined (sequence_id, id));



CREATE TABLE primers (sequence_id integer NOT NULL,id integer NOT NULL,primer integer NOT NULL,left_p text NOT NULL,left_sequence text NOT NULL,left_tm float NULL,left_gc float NULL,left_self_end float NULL,left_self_any float NULL,left_hairpin float NULL,left_end_stability float NULL,left_penalty float NULL,right_p text NOT NULL,right_sequence text NOT NULL,right_tm float NULL,right_gc float NULL,right_self_end float NULL,right_self_any float NULL,right_hairpin float NULL,right_end_stability float NULL,right_penalty float NULL,pair_product_size float NULL,pair_compl_end float NULL,pair_compl_any float NULL,pair_penalty float NULL,
	
	FOREIGN KEY (sequence_id, id) REFERENCES combined (sequence_id, id));

CREATE TABLE primers2 (id integer primary key autoincrement, sequence_id integer NOT NULL,combined_id integer NOT NULL,primer integer NOT NULL,left_p text NOT NULL,left_sequence text NOT NULL,left_tm float NULL,left_gc float NULL,left_self_end float NULL,left_self_any float NULL,left_hairpin float NULL,left_end_stability float NULL,left_penalty float NULL,right_p text NOT NULL,right_sequence text NOT NULL,right_tm float NULL,right_gc float NULL,right_self_end float NULL,right_self_any float NULL,right_hairpin float NULL,right_end_stability float NULL,right_penalty float NULL,pair_product_size float NULL,pair_compl_end float NULL,pair_compl_any float NULL,pair_penalty float NULL,FOREIGN KEY (sequence_id, combined_id) REFERENCES combined (sequence_id, id));



CREATE TABLE tagged_primers (sequence_id integer NOT NULL,
id integer NOT NULL,primer integer NOT NULL,best integer NOT NULL,tag text NULL,tagged text NULL,tag_seq text NULL,common text NULL,pigtail_tagged text NULL,pigtail_tag_seq text NULL,pigtail_common text NULL,left_p text NULL,left_sequence text NULL,left_self_end float NULL,left_self_any float NULL,left_hairpin float NULL,left_penalty float NULL,right_p text NULL,right_sequence text NULL,right_self_end float NULL,right_self_any float NULL,right_hairpin float NULL,right_penalty float NULL,pair_product_size float NULL,pair_compl_end float NULL,pair_compl_any float NULL,pair_penalty float NULL,FOREIGN KEY (sequence_id, id) REFERENCES combined (sequence_id, id));

CREATE INDEX combined_members_idx on combined (members);

CREATE INDEX seq_name_idx on sequence (name);
