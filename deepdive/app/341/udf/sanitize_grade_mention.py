#! /usr/bin/env python

import csv, os, sys

# The directory of this UDF file
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

########################## Spelling Correction Setup ############################
# read in feature definitions
spellingMappingFilename = BASE_DIR + "/grade_keywords_sanitized.txt"
spellingMapping=[]
with open(spellingMappingFilename, 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
	for row in csvreader:
		spellingMapping.append(row)

# ith key in mispelled is associated with ith correction
correction = [spellingMapping[i][0] for i in xrange(len(spellingMapping))]
mispelled = [spellingMapping[i][1] for i in xrange(len(spellingMapping))]
################################################################################

# For-loop for each row in the input query
for row in sys.stdin:
  # Find phrases that are continuous words tagged with PATIENT
  patient_id, senetence_id, start_position, length, lemma_phrase, word_phrase, mention_id = row.strip().split('\t')
  lemmas = lemma_phrase.split(" ")
  correct_words =  "";
  for lemma in lemmas:
    if lemma.lower() in mispelled:
      correct_words += correction[mispelled.index(lemma.lower())] + " "
    else:
      correct_words += lemma.lower() + " "
  correct_words = correct_words[:-1]

  print '\t'.join([
    patient_id, 
    senetence_id, 
    start_position, 
    length, 
    correct_words, 
    word_phrase, 
    mention_id 
    ])

