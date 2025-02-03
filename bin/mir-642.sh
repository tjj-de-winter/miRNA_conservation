# get miR-642 FASTA

mirbase_link=https://www.mirbase.org/download/mature.fa
fasta=hsa-miR-642.fasta

wget $mirbase_link

mirbase=$(basename $mirbase_link)

cat $mirbase | grep -A 1 "hsa-miR-642" | grep -A 1 "3p" | grep -v "^--$" > $fasta

