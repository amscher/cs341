#! /usr/bin/env python

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

dictionaryFileName = '/Users/jackywang/Desktop/341/deepDive/app/spouse/udf/test'
with open(dictionaryFileName, 'rb') as inputfile:
  keywords = [row[:-1] for row in inputfile]

# For-loop for each row in the input query
for row in sys.stdin:
  # Find phrases that are continuous words tagged with PERSON.
  patient_id, sentence_id, words_str, lemma_str = row.strip().split('\t')
  words = words_str.split(ARR_DELIM)
  lemmas = lemma_str.split(ARR_DELIM)
  start_index = 0
  phrases = []

  while start_index < len(words):
    # Checking if there is a grade related phrase starting from start_index
    index = start_index
    while 1:
      if index < len(words) and lemmas[index] in keywords:
        index += 1
      elif index+1 < len(words) and lemmas[index] + ' ' + lemmas[index+1] in keywords:
        index += 2
      else:
        break

    if index != start_index:   # found a person from "start_index" to "index"
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
        '%s_%d' % (patient_id, start_position)        # mention_id
      ]])