#! /usr/bin/env python

import csv, os, sys
import re

# Sample input data (piped into STDIN):
'''
patient_id sentence_id words('~^~') lemma('~^~')
'''
import sys

#################################################
# This function is not used, as it is too slow O(n^2)
def editDist(correct, misspelled, limit):
  if (len(correct) == 0 or len(misspelled) == 0):
    return len(correct) + len(misspelled)
  if limit < 0:
    return 1

  if (correct[0] == misspelled[0]):
    return editDist(correct[1:], misspelled[1:], limit)
  return min(editDist(correct, misspelled[1:], limit-1), editDist(correct[1:], misspelled, limit-1), editDist(correct[1:], misspelled[1:], limit-1)) + 1

##################################################
ARR_DELIM = '~^~'

# The directory of this UDF file
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

dictionaryFileName = BASE_DIR + '/grade_keywords.txt'
with open(dictionaryFileName, 'rb') as inputfile:
  keywords = [row[:-1] for row in inputfile]

# For-loop for each row in the input query
for row in sys.stdin:
  # Find phrases that are continuous words tagged with PERSON.
  if len(row.strip().split('\t')) < 4:
    continue
  patient_id, sentence_id, words_str, lemma_str = row.strip().split('\t')
  words = words_str.split(ARR_DELIM);
  lemmas = lemma_str.split(ARR_DELIM);

  start_index = 0
  phrases = []

  while start_index < len(words):
    # Checking if there is a grade related phrase starting from start_index
    index = start_index
    while 1:
      if index < len(words) and lemmas[index].lower() in keywords:
        index += 1
        if index+1 < len(words) and lemmas[index] in [":", "4", "3", "2", "1"]:
          index += 1
      else:
        break

    if index != start_index:   # found a grade mention from "start_index" to "index"
      lemma_phrase = ' '.join(lemmas[start_index:index])
      word_phrase = ' '.join(words[start_index:index])
      length = index - start_index
      phrases.append((start_index, length, lemma_phrase, word_phrase))
    start_index = index + 1

  # Output a tuple for each grade related phrase
  for start_position, length, lemma_phrase, word_phrase in phrases:
    print '\t'.join(
      [ str(x) for x in [
        patient_id,
        sentence_id,
        start_position,   # start_position
        length, # length
        lemma_phrase,  # phrase of concatenated root words
        word_phrase,
        '%s_%d' % (sentence_id, start_position)        # mention_id
      ]])
