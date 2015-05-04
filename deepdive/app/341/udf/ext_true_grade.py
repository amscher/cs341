#! /usr/bin/env python

import csv, os, sys
import re

# The directory of this UDF file
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

true_grades_file = BASE_DIR + '/old_true_grades_multi.csv'

recorded_id = set()
for row in sys.stdin:
  patient_id = row.strip()
  recorded_id.add(patient_id)

patient_grade_set = set()
with open(true_grades_file, 'rb') as inputfile:
  for row in inputfile:
    patient_id, grade = row.strip().split(',')
    patient_grade_set.add((patient_id, grade))
    if patient_id in recorded_id:
      print '\t'.join([
        patient_id,
        grade,
        '\N' # leave "id" blank for system!
        ])
