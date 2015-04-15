DROP TABLE IF EXISTS sentences CASCADE;
CREATE TABLE sentences(
  document_id text, -- patiend_id text
  sentence text,  -- sentence_id text
  words text[], -- sentence text
  lemma text[], -- words text[]
  pos_tags text[], -- lemma text[]
  dependencies text[], -- postag text
  ner_tags text[], -- dependecies text[]
  sentence_offset bigint,
  sentence_id text -- unique identifier for sentences
  );


DROP TABLE IF EXISTS people_mentions CASCADE;
CREATE TABLE people_mentions(
  patient_id text, -- patient_id
  sentence_id text, -- sentence_id
  start_position int, -- start_position
  length int,  -- length
  lemma_phrase text, -- phrase of root words 
  word_phrase text, -- phrase of document words
  mention_id text  -- unique identifier for people_mentions ( sentence_id + start_position)
  );

DROP TABLE IF EXISTS stage_t_mentions CASCADE;
CREATE TABLE stage_t_mentions(
  patient_id text, -- patient_id
  sentence_id text, -- sentence_id
  start_position int, -- start_position
  length int,  -- length
  lemma_phrase text, -- phrase of root words 
  word_phrase text, -- phrase of document words
  mention_id text  -- unique identifier for tumour_t_mentions ( sentence_id + start_position)
  );


DROP TABLE IF EXISTS has_spouse CASCADE;
CREATE TABLE has_spouse(
  person1_id text,
  person2_id text,
  sentence_id text,
  description text,
  is_true boolean,
  relation_id text, -- unique identifier for has_spouse
  id bigint   -- reserved for DeepDive
  );

DROP TABLE IF EXISTS has_spouse_features CASCADE;
CREATE TABLE has_spouse_features(
  relation_id text,
  feature text);
