#! /usr/bin/env python

import csv, os, sys
import re

# Sample input data (piped into STDIN):
ARR_DELIM = '~^~'
BETWEEN_RATIO = 1.2 # ratio between the highest weight and the second highest such that it's a between grade

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
  patient_id, mention_id, lemma_phrase = row.strip().split('\t')
  mention_ids = mention_id.split(ARR_DELIM);
  lemmas = lemma_phrase.split(ARR_DELIM);
  
  # Create the data structure for identifying which grade has most weight
  featureBins = [[] for i in xrange(5)]

  # Looping over all lemmas to populate the featureBins
  for i in xrange(len(lemmas)):
    lemma = lemmas[i].lower()
    tokens = lemma.split(" ");
    for token in tokens:
      if token in keys:
        ind = keys.index(token)
        label = labels[ind]
        weight = weights[ind]
        featureBins[label].append((token, weight, mention_ids[i]))
    
  # Tally featureBins
  tallyBins = [0 for i in xrange(5)]

  # Looping over special keywords like "grade", "differentiate"
  for sp_token, sp_weight, sp_mention_id in featureBins[0]:
    sp_sent_id = int(sp_mention_id.split("_")[1])
    for grade in xrange(1,5):
      for token, weight, mention_id in featureBins[grade]:
        sent_id = int(mention_id.split("_")[1])
        tallyBins[grade] += max(0, sp_weight - abs(sp_sent_id - sent_id))

  # Looping over remaining grade keywords
  for grade in xrange(1,5):
    for token, weight, mention_id in featureBins[grade]:
      sent_id = int(mention_id.split("_")[1])
      tallyBins[grade] += weight
 
  # Find the most weight (highest to lowest)
  sortedIndex = [i[0] for i in sorted(enumerate(tallyBins), key=lambda x:-x[1])]
  if sum(tallyBins) == 0:
    predicted_grade = str(0)
    predictedFeatures = []
    unpredictedFeatures = []
    for i in xrange(5):
      unpredictedFeatures += featureBins[i]
  else:
    # Directly add the special words into predicted_grade
    sortedIndex.remove(0)

    if ( BETWEEN_RATIO *tallyBins[sortedIndex[1]] > tallyBins[sortedIndex[0]] and 
         abs(sortedIndex[1] - sortedIndex[0]) <= 1 ):
      # transition between two grades
      predicted_grade = str((sortedIndex[0]+sortedIndex[1])/2.0)
      predictedFeatures = featureBins[sortedIndex[0]] + featureBins[sortedIndex[1]] 
      unpredictedFeatures = featureBins[sortedIndex[2]] + featureBins[sortedIndex[3]]
    else:
      predicted_grade = str(sortedIndex[0])
      predictedFeatures = featureBins[sortedIndex[0]]  
      unpredictedFeatures = featureBins[sortedIndex[1]] + featureBins[sortedIndex[2]] + featureBins[sortedIndex[3]]
    '''
    # Put the special words either into predicted_features or unpredictedFeatures depending on if they are close to
    # predicted features
    for sp_feature in featureBins[0]:
      sp_token, sp_weight, sp_mention_id = sp_feature
      sp_sent_id = int(sp_mention_id.split("_")[1])
      for token, weight, mention_id in predictedFeatures:
        sent_id = int(mention_id.split("_")[1])
        if ( sp_weight - abs(sp_sent_id - sent_id) > 0 ):
          predictedFeatures.append(sp_feature)
        else:
          unpredictedFeatures.append(sp_feature)
    '''
  # Prepare output to table
  predict_words = []
  predict_mention_ids = []
  unpredict_words = []
  unpredict_mention_ids = []
  for token, weight, mention_id in predictedFeatures:
    predict_words.append(formatForToken(token))
    predict_mention_ids.append(mention_id)
  for token, weight, mention_id in unpredictedFeatures:
    unpredict_words.append(formatForToken(token))
    unpredict_mention_ids.append(mention_id)
  
  '''
  # DEBUG START
  predicted_grade = str(1)
  predict_words = lemmas
  predict_mention_ids = mention_ids
  unpredict_words = []
  unpredict_mention_ids = []
  # DEBUG END
  '''
  
  # print out...
  print '\t'.join([
                  patient_id,
                  predicted_grade,
                  array_to_str(predict_words), 
                  array_to_str(predict_mention_ids),
                  array_to_str(unpredict_words),
                  array_to_str(unpredict_mention_ids)
                  ])

