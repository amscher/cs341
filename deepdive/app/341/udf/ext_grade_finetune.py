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
  patient_id, mention_id, lemma_phrase = row.strip().split('\t')
  mention_ids = mention_id.split(ARR_DELIM);
  lemmas = lemma_phrase.split(ARR_DELIM);
  
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
   
    
  # Tally featureBins
  tallyBins = [0 for i in xrange(5)]

  # Looping over special keywords like "grade", "differentiate"
  for sp_token, sp_weight, sp_mention_id in featureBins[0]:
    sp_sent_id = int(sp_mention_id.split("_")[1])
    sp_prefix = sp_weight < 0 # if the special token is a prefix ie grade
    # Finding the sentence distance is to ensure if there is 1 keyword that
    # is in same sentence as in the special token, then only those keywords in 
    # same sentence get higher weights
    sent_dist = [int(mention_id.split("_")[1]) - sp_sent_id \
                  for grade in xrange(1,5) \
                  for token, weight, mention_id in featureBins[grade]]

    sp_in_same_sentence = 0 in sent_dist
    for grade in xrange(1,5):
      for token, weight, mention_id in featureBins[grade]:
        sent_id = int(mention_id.split("_")[1])
        if ( (not sp_in_same_sentence) or (sent_id - sp_sent_id == 0) ):
          # Limit the distance that sp can affect and linearly tailored the weight
          dist = sp_sent_id - sent_id
          if (sp_prefix and -SP_DIST < dist and dist <= 0) or \
             (not sp_prefix and dist >= 0 and dist < SP_DIST):
            #tallyBins[grade] += abs(sp_weight)/SP_DIST * max(0, SP_DIST - max(0, sent_id - sp_sent_id))
            tallyBins[grade] += abs(sp_weight)/SP_DIST * (SP_DIST - abs(dist))
          #elif not sp_prefix and 
          #  tallyBins[grade] += abs(sp_weight)/SP_DIST * max(0, SP_DIST - max(0, sp_sent_id - sent_id))

        

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

    if ( BETWEEN_RATIO * tallyBins[sortedIndex[1]] > tallyBins[sortedIndex[0]] and 
         abs(sortedIndex[1] - sortedIndex[0]) <= 1 ):
      # transition between two grades
      predicted_grade = str((sortedIndex[0]+sortedIndex[1])/2.0)
      predictedFeatures = featureBins[sortedIndex[0]] + featureBins[sortedIndex[1]] 
      unpredictedFeatures = featureBins[sortedIndex[2]] + featureBins[sortedIndex[3]]
    else:
      predicted_grade = str(sortedIndex[0])
      predictedFeatures = featureBins[sortedIndex[0]]  
      unpredictedFeatures = featureBins[sortedIndex[1]] + featureBins[sortedIndex[2]] + featureBins[sortedIndex[3]]
    
    # Put the special words either into predicted_features or unpredictedFeatures depending on if they are close to
    # predicted features
    for sp_feature in featureBins[0]:
      sp_token, sp_weight, sp_mention_id = sp_feature
      sp_sent_id = int(sp_mention_id.split("_")[1])
      sp_used_to_predict = False
      sp_prefix = sp_weight < 0
      
      sent_dist = [int(mention_id.split("_")[1]) - sp_sent_id \
                  for grade in xrange(1,5) \
                  for token, weight, mention_id in featureBins[grade]]

      sp_in_same_sentence = 0 in sent_dist
      # Loop through to find if special token is used in predicted feature
      for token, weight, mention_id in predictedFeatures:
        sent_id = int(mention_id.split("_")[1])
        
        if ( (not sp_in_same_sentence) or (sent_id - sp_sent_id == 0) ):
          # Limit the distance that sp can affect and linearly tailored the weight
          dist = sp_sent_id - sent_id
          if (sp_prefix and -SP_DIST < dist and dist <= 0) or \
             (not sp_prefix and dist >= 0 and dist < SP_DIST):
            sp_used_to_predict = True
            break
      # Update features correspondingly
      if (sp_used_to_predict):
        predictedFeatures.append(sp_feature)
      else:
        unpredictedFeatures.append(sp_feature)
    
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
  
  # DEBUG START
  #predicted_grade = str(1)
  #predict_words = lemmas
  #predict_mention_ids = mention_ids
  #unpredict_words = []
  #unpredict_mention_ids = []
  weight_str = ""
  for i in xrange(len(tallyBins)):
    weight_str += str(tallyBins[i]) + " "
  # DEBUG END
  
  # print out...
  print '\t'.join([
                  patient_id,
                  predicted_grade,
                  array_to_str(predict_words), 
                  array_to_str(predict_mention_ids),
                  array_to_str(unpredict_words),
                  array_to_str(unpredict_mention_ids),
                  weight_str
                  ])

