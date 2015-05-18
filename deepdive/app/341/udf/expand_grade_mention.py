#! /usr/bin/env python

import csv, os, sys, re

# The directory of this UDF file
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# For-loop for each row in the input query
for row in sys.stdin:
  # Find phrases that are continuous words tagged with PATIENT
  patient_id, senetence_id, start_position, length, lemma_phrase, word_phrase, mention_id = row.strip().split('\t')
  print '\t'.join([
    patient_id, 
    senetence_id, 
    start_position, 
    length, 
    lemma_phrase, 
    word_phrase, 
    mention_id 
    ])

  if int(length) > 1:
    lemmas = re.split('~|-|/| ', lemma_phrase);
    for i in xrange(len(lemmas)):
      lemma = lemmas[i]
      print '\t'.join([
        patient_id, 
        senetence_id, 
        start_position, 
        str(1), 
        lemma, 
        word_phrase, 
        senetence_id + "_" + str(int(start_position) + i)
        ])

