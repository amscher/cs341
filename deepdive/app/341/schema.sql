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
  true_grade text,
  id bigint --reserved for deepdive inference
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

DROP TABLE IF EXISTS grade_features CASCADE;
CREATE TABLE grade_features(
    patient_id text,
    feature text
  );

