import Sentence
import re
from os import listdir
from os.path import isfile, join, isdir

punctuationToRemove = set([',', '}', '{', '\\', ' ', '\"'])

def formatForToken(s):
  if punctuationToRemove.intersection(s):
    return '\"\"'+s+'\"\"'
  return s

for dir in listdir("../RS_PATH.62"):
  if not isdir("../RS_PATH.62/" + dir):
    continue
  patient_id = dir[0:12]
  if isfile("../RS_PATH.62/" + dir + "/input.text"):
    print patient_id
    input = open("../RS_PATH.62/" + dir + "/input.text", 'r')
    output = open("csv_output/" + patient_id + ".csv", 'w')
    line = input.readline()
    sent = Sentence.Sentence(patient_id, patient_id+"SENT_1")
    while line:
      if line.strip():
        tokens = line.split()
        if tokens[0] == '1' and not len(sent.words) == 0:
          output.write(sent.to_string() + "\n")
          sent = Sentence.Sentence(patient_id, patient_id+tokens[7])
        #if (tokens[1] not in punctuationToRemove \
        #    and tokens[4] not in punctuationToRemove):
        
        orig = tokens[1].replace('"','\"\"');
        sent.orig.append(orig)
        
        
        tokens[1] = tokens[1].replace('\\','\\\\')
        tokens[4] = tokens[4].replace('\\','\\\\')
        tokens[1] = tokens[1].replace('"','\\\"\"')
        tokens[4] = tokens[4].replace('"','\\\"\"')
        
        sent.words.append(formatForToken(tokens[1]))
        sent.lemma.append(formatForToken(tokens[4]))
        sent.dep_tags.append(formatForToken(tokens[6]))
        sent.pos_tags.append(formatForToken(tokens[2]))
        #if punctuationToRemove.intersection(tokens[1]):
        #  sent.words.append('\"\"'+tokens[1]+'\"\"')
        #else:
        #  sent.words.append(tokens[1])
        
        #if punctuationToRemove.intersection(tokens[4]):
        #  sent.lemma.append('\"\"'+tokens[4]+'\"\"')
        #else:
        #  sent.lemma.append(tokens[4])
        
        #if punctuationToRemove.intersection(tokens[6]):
        #  sent.dep_tags.append('\"\"'+tokens[6]+'\"\"')
        #else:
        #  sent.dep_tags.append(tokens[6])
        
        #if punctuationToRemove.intersection(tokens[2]):
        #  sent.pos_tags.append('\"\"'+tokens[2]+'\"\"')
        #else:
        #  sent.pos_tags.append(tokens[2])
        
        #sent.dep_tags.append(tokens[6])
        #sent.pos_tags.append(tokens[2])
      line = input.readline()
    output.write(sent.to_string() + "\n")

    output.close()
    input.close()
