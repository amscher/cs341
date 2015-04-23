#!/usr/bin/env bash
set -eu

: ${corpus_root:=corpus}

read header
echo pdf_url
while read patient_id; do
  pdfpath=$(ls $corpus_root/$patient_id.*/input_*.pdf | head -1) || continue
  echo $pdfpath
done
