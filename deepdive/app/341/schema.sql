DROP TABLE IF EXISTS sentences CASCADE;
CREATE TABLE sentences(
  patient_id text,
  sentence_id text, -- unique identifier for sentences
  sentence text,
  words text[],
  lemma text[],
  pos_tags text[],
  dependencies text[],
  ner_tags text[]
  );

DROP TABLE IF EXISTS true_grades CASCADE;
CREATE TABLE true_grades(
  patient_id text,
  true_grade text
 );

DROP TABLE IF EXISTS grade_mentions CASCADE;
CREATE TABLE grade_mentions(
    patient_id text,
    sentence_id text, --patient_id + sent
    start_position text,   -- start_position
    length text, -- length
    lemma_phrase text,  -- phrase of concatenated root words
    word_phrase text,
    mention_id text --sentence_id + start_id
  );

DROP TABLE IF EXISTS grade_candidates CASCADE;
CREATE TABLE grade_candidates(
    patient_id text,
    grade text, --predicted grade
    predict_words text, --words led to prediction
    predict_mention_id text, --mention id corresponding to predict 
    nonpredict_words text,  --words not used for prediction
    nonpredict_mention_id text, --mention id corresponding to nonpredict words
    weights text -- debugging purpose, weight of all labels
  );

DROP TABLE IF EXISTS has_1 CASCADE;
CREATE TABLE has_1(
  person1_id text,
  person2_id text,
  sentence_id text,
  description text,
  is_true boolean,
  relation_id text, -- unique identifier for has_spouse
  id bigint   -- reserved for DeepDive
  );


DROP TABLE IF EXISTS has_2 CASCADE;
CREATE TABLE has_2(
  person1_id text,
  person2_id text,
  sentence_id text,
  description text,
  is_true boolean,
  relation_id text, -- unique identifier for has_spouse
  id bigint   -- reserved for DeepDive
  );


DROP TABLE IF EXISTS has_3 CASCADE;
CREATE TABLE has_3(
  person1_id text,
  person2_id text,
  sentence_id text,
  description text,
  is_true boolean,
  relation_id text, -- unique identifier for has_spouse
  id bigint   -- reserved for DeepDive
  );



DROP TABLE IF EXISTS has_4 CASCADE;
CREATE TABLE has_4(
  person1_id text,
  person2_id text,
  sentence_id text,
  description text,
  is_true boolean,
  relation_id text, -- unique identifier for has_spouse
  id bigint   -- reserved for DeepDive
  );


DROP TABLE IF EXISTS has_grade_features CASCADE;
CREATE TABLE has_grade_features(
  relation_id text,
  feature text);
