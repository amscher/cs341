psql deepdive-grades -c "
COPY (
(select distinct patient_id from sentences)
except
(select distinct patient_id from grade_mentions)
) TO STDOUT CSV HEADER;" >items.csv

paste -d, items.csv <(./add_pdf_url.sh <items.csv) >items-with-pdf.csv 
