import Sentence
from os import listdir
from os.path import isfile, join, isdir

for dir in listdir("RS_PATH.62"):
  # print dir[0:4]
  if not isdir("RS_PATH.62/" + dir):
    continue
  patient_id = dir[0:12]
  if isfile("RS_PATH.62/" + dir + "/input.text"):
    print patient_id
    input = open("RS_PATH.62/" + dir + "/input.text", 'r')
    output = open("csv_output/" + patient_id + ".csv", 'w')
    line = input.readline()
    sent = Sentence.Sentence(patient_id, patient_id+"SENT_1")
    while line:
      if line.strip():
        tokens = line.split()
        if tokens[0] == '1' and not len(sent.words) == 0:
          output.write(sent.to_string() + "\n")
          sent = Sentence.Sentence(patient_id, patient_id+tokens[7])
        sent.words.append(tokens[1])
        sent.lemma.append(tokens[4])
        sent.pos_tags.append(tokens[2])
      line = input.readline()
    output.write(sent.to_string() + "\n")

    output.close()
    input.close()