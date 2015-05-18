#! /usr/bin/env python

import csv, os, sys, re

'''
patient_id lemma_phrase(~^~) mention_id(~^~) length(~^~)
'''
ARR_DELIM = '~^~'

features = []
tokens = []
# For-loop for each row in the input query
for row in sys.stdin:
  # Find phrases that are continuous words tagged with PATIENT
  patient_id, lemma_phrase, mention_id, length = row.strip().split('\t')
  lemmas = lemma_phrase.split(ARR_DELIM)
  mention_ids = mention_id.split(ARR_DELIM)
  lengths = map(int, length.split(ARR_DELIM))

  for i in xrange(len(lemmas)):
    lemma = lemmas[i]

    # Occurence of the phrase by itself
    features.append(lemma)

    # Binary Pairs
    if lengths[i] == 1 and len(lemma) > 0:
      tokens.append(lemma)

# Enumerate all possible binary tokens (sorted)
tokens = list(set(tokens))
tokens.sort()
pairsOccurence = [tokens[i] + "@^@" + tokens[j] for i in xrange(len(tokens)) for j in xrange(i+1, len(tokens))]
for p in pairsOccurence:
  features.append(p)

features = list(set(features))
for feature in features:
  print feature