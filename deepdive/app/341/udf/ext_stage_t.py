#! /usr/bin/env python

# Sample input data (piped into STDIN):
'''
patient_id sentence_id words('~^~') lemma('~^~')
'''
def hasNumber(inputString):
  return any(char.isdigit() for char in inputString)

import sys
ARR_DELIM = '~^~'

keywordsFileName = '/Users/jackywang/Desktop/341/deepDive/app/spouse/udf/stage_t_keywords'
szKeywordsFileName = '/Users/jackywang/Desktop/341/deepDive/app/spouse/udf/stage_t_sentence_keywords'
tumorSpellings = ['tumour', 'tumor']

with open(keywordsFileName, 'rb') as inputfile:
  keywords = [row[:-1] for row in inputfile]
with open(szKeywordsFileName, 'rb') as inputfile:
  sz_keywords = [row[:-1] for row in inputfile]


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
    
    # sentence has "tumor" in it, examine for size info
    if (lemmas[index] in tumorSpellings):
      tumor_sz_start_index = 0
      while tumor_sz_start_index < len(words):
        tumor_sz_index = tumor_sz_start_index
        while tumor_sz_index < len(words) and \
          lemmas[tumor_sz_index] not in keywords and \
          (hasNumber(lemmas[tumor_sz_index]) or lemmas[tumor_sz_index] in sz_keywords):
            tumor_sz_index += 1
        if tumor_sz_index != tumor_sz_start_index:
          # found size related phrase
          lemma_phrase = ' '.join(lemmas[tumor_sz_start_index:tumor_sz_index])
          word_phrase = ' '.join(words[tumor_sz_start_index:tumor_sz_index])
          length = tumor_sz_index - tumor_sz_start_index
          phrases.append((tumor_sz_start_index, length, lemma_phrase, word_phrase))
        tumor_sz_start_index = tumor_sz_index + 1
    
    # regular check for "pT1", "T1", "pT 1"...
    while 1:
      if index < len(words) and lemmas[index] in keywords:
        if hasNumber(lemmas[index]):
          index += 1
        elif index+1 < len(words) and hasNumber(lemmas[index+1]):
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
