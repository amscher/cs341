#! /usr/bin/env python

import csv, os, sys
import re

# Sample input data (piped into STDIN):
ARR_DELIM = '~^~'
BETWEEN_RATIO = 1.2 # ratio between the highest weight and the second highest such that it's a between grade
SP_DIST = 2

'''
patient_id sentence_id(~^~) start_position(~^~)  mention_id(~^~)  lemma_phrase(~^~) 
'''

punctuationToRemove = set([',', '}', '{', '\\', ' ', '\"'])

def formatForToken(s):
  s = s.replace('"','\"\"');
  s = s.replace('\\','\\\\')
  s = s.replace('"','\\\"\"')
  if punctuationToRemove.intersection(s):
    return '\"\"'+s+'\"\"'
  return s

def array_to_str(array):
  arr_str = "\"{"
  for i in range(len(array)):
    arr_str += array[i]
    if (i < len(array) - 1):
      arr_str += ","
  arr_str += "}\""
  return arr_str


# The directory of this UDF file
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

########################## Label/Weight/Keys Setup ############################
# read in feature definitions
featureDefinitionFilename = BASE_DIR + "/grade_keywords_class_weight.txt"
featureDefinition=[]
with open(featureDefinitionFilename, 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
	for row in csvreader:
		featureDefinition.append(row)

# ith key in keys is associated with ith label in labels and ith weight in weights
# labels == grades, except when labels = 0 
# label = 0, that's for special, emphatic keywords like "grade", "g", "differentiate"
labels = [int(featureDefinition[i][0]) for i in xrange(len(featureDefinition))]
weights = [int(featureDefinition[i][1]) for i in xrange(len(featureDefinition))]
keys = [featureDefinition[i][2] for i in xrange(len(featureDefinition))]
################################################################################


# For-loop for each row in the input query
for row in sys.stdin:
  # Find phrases that are continuous words tagged with PATIENT
  patient_id, mention_id, lemma_phrase, grade = row.strip().split('\t')
  mention_ids = mention_id.split(ARR_DELIM);
  lemmas = lemma_phrase.split(ARR_DELIM);
  grade = grade.strip()

  '''
  # Create the data structure for identifying which grade has most weight
  featureBins = [[] for i in xrange(5)]

  # Looping over all lemmas to populate the featureBins
  for i in xrange(len(lemmas)):
    lemma = lemmas[i].lower()
    tokens = lemma.split(" ")
    for token in tokens:
      if token in keys:
        ind = keys.index(token)
        label = labels[ind]
        weight = weights[ind]
        featureBins[label].append((token, weight, mention_ids[i]))
      else:
        subtokens = re.split('~|-|/', token)
        for subtoken in subtokens:
          if subtoken in keys:
            ind = keys.index(subtoken)
            label = labels[ind]
            weight = weights[ind]
            featureBins[label].append((subtoken, weight, mention_ids[i]))
  
  features = set()

  # Looping over special keywords like "grade", "differentiate"
  for sp_token, sp_weight, sp_mention_id in featureBins[0]:
    sp_patient_id, sp_sent_id, sp_start_id = sp_mention_id.split("_")
    sp_sent_id = int(sp_sent_id)
    sp_start_id = int(sp_start_id)
    for grade in xrange(1,5):
      for token, weight, mention_id in featureBins[grade]:
        patient_id, sent_id, start_id = mention_id.split("_")
        sent_id = int(sent_id)
        start_id = int(start_id)
        #features.add("word_between=%s_%s_%d" % (sp_token, token, sp_sent_id - sent_id)) 
        #features.add("word_between_%s_%s=%d" % (sp_token, token, sp_sent_id - sent_id)) 
        features.add("word_between=%s_%s" % (sp_token, token)) 

  for feature in features:
    print str(patient_id) + '\t' + feature
  '''
  print patient_id + '\t' + grade
