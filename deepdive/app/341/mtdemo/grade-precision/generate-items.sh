psql deepdive-grades -c "
COPY (
select m.patient_id,*
from grade_mentions m,sentences s
where m.sentence_id = s.sentence_id
  and m.patient_id = s.patient_id
order by random()
limit 200
) TO STDOUT CSV HEADER;" >items.csv

paste -d, items.csv <(./add_pdf_url.sh <items.csv) >items-with-pdf.csv 
