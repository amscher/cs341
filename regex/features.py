# features.py
#
# extract text features to csv file
#
# Kun-Hsing Yu
# 2015.04.20

import os
import csv

path="/Users/khyu/Dropbox/tcgaLUAD/tcgaLUADpath/curated/"
featureDefinitionFilename="/Users/khyu/Dropbox/tcgaLUAD/tcgaLUADpath/scripts/version2/featureDefinition.txt"

os.system("clear")
os.system("date")

# read in feature definitions
featureDefinition=[]

with open(featureDefinitionFilename, 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
	for row in csvreader:
		print row
		featureDefinition.append(row)

for i in range(len(featureDefinition)):
	featureDefinition[i][0]=int(featureDefinition[i][0])

nFeature=featureDefinition[len(featureDefinition)-1][0]



# read in all file names
osFilelist=os.popen("ls " + path + "*/*")
osFilelist=osFilelist.read()
osFilelist=osFilelist.split('\n')

nFile=len(osFilelist)-1

features=[[0 for x in xrange(nFeature+2)] for x in xrange(nFile)] 

for i in range(nFile):
	features[i][0]=osFilelist[i]
	keyStart=features[i][0].find("TCGA-")
	features[i][1]=osFilelist[i][keyStart:(keyStart+12)]
# populate column names (not implemented)

# read in text features
# grep -li list files with matches + ignore upper/lower cases
for itemFeature in range(len(featureDefinition)):
	osOutputRaw=os.popen("grep -li '" + featureDefinition[itemFeature][1] + "' " + path + "*/*")
	osOutput=osOutputRaw.read()
	osOutput=osOutput.split('\n')
	for itemOsOutput in range(len(osOutput)-1):
		for itemNFile in range(nFile):
			if (features[itemNFile][0]==osOutput[itemOsOutput]):
				#print featureDefinition[itemFeature][0]
				#print osOutput[itemOsOutput]
				features[itemNFile][featureDefinition[itemFeature][0]+1]=1


#osOutputRaw=os.popen("grep -li 'poorly differentia' " + path + "*/*")
#osOutput=osOutputRaw.read()
#osOutput=osOutput.split('\n')

with open('features.csv', 'w') as fp:
    csvwriter = csv.writer(fp, delimiter=',')
    csvwriter.writerows(features)
