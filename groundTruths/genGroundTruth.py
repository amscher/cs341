import csv
cancerType = 'LUSC'

inputFileName = 'tcga'+cancerType+'Grade.csv'
outputFileName = 'tcga'+cancerType+'GradeTruth.tsv'
gradeList = ['1','1.5','2','2.5','3','3.5','4']
gradeDict = {x : set() for x in gradeList}
with open(outputFileName, 'wb') as outputfile:
  with open(inputFileName, 'rb') as inputfile:
    reader = csv.DictReader(inputfile)
    for row in reader:
      if row['Grade'] == 'X' or row['Grade'] == 'x':
        continue
      gradeDict[row['Grade']].add(row['TCGA_ID'][:12])

  for grade in gradeList:
    patientSet = gradeDict[grade]
    for patientId in patientSet:
      outputfile.write("%s\t%s\n" % (patientId, grade))


inputFileName = 'tcga'+cancerType+'Clinical.csv'
outputFileName = 'tcga'+cancerType+'StageTruth.tsv'
stageList = ['Stage I','Stage IA','Stage IB','Stage II','Stage IIA','Stage IIB','Stage III','Stage IIIA','Stage IIIB','Stage IV','Stage IVA','Stage IVB']
stageDict = {x : set() for x in stageList}
with open(outputFileName, 'wb') as outputfile:
  with open(inputFileName, 'rb') as inputfile:
    reader = csv.DictReader(inputfile)
    for row in reader:
      print row['pathologic_stage'], row['pathologic_stage'] == '[Not Available]'
      if row['pathologic_stage'] == "[Not Available]":
        continue
      stageDict[row['pathologic_stage']].add(row['bcr_patient_barcode'][:12])

  for stage in stageList:
    patientSet = stageDict[stage]
    for patientId in patientSet:
      outputfile.write("%s\t%s\n" % (patientId, stage))

print "Done converting"
