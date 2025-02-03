#!/bin/bash
# Based on 3UTReQTL_islets/bin/eQTL_miRanda.sh

### Description ###

# Compute miRanda binding scores for a set of mature miRNAs and target sites.

f1=human_CMTM6.fasta # ./human.sh
f2=mouse_Cmtm6.fasta # ./mouse.sh
f3=rat_Cmtm6.fasta # ./rat.sh
mature_mirna_fasta_file=hsa-miR-642.fasta # ./mir-642.sh
output_path=./miranda
outprefix=CMTM6_hsa-miR-642
target_fasta_file=CMTM6_seqs.fasta

mkdir -p ${output_path}

outprefix=${output_path%/}/${outprefix}

### Parameters ###
score_threshold=140
energy_threshold=1
scale_Z=4
gap_open=-4
gap_extend=-9

### Paths to utilities and scripts###
p2miranda=$(which miranda)

### Code ###

# Merge the reference and alternative FASTA file into one file
cat ${f1} > ${target_fasta_file}
cat ${f2} >> ${target_fasta_file}
cat ${f3} >> ${target_fasta_file}

# Compute the alignment and energy scores for each miRNA and eQTL pair
miranda_out_file=${outprefix}.miranda.out.txt
echo "start generating ${miranda_out_file}"
${p2miranda} ${mature_mirna_fasta_file} ${target_fasta_file} -sc ${score_threshold} -en ${energy_threshold} -scale ${scale_Z} -go ${gap_open} -ge ${gap_extend} -out ${miranda_out_file}

# export data to CSV file
miranda_csv_file=${outprefix}.miranda.out.csv
cat ${miranda_out_file} |\
 grep -A 1 "Scores for this hit:" |\
 grep -v "Scores for this hit:" |\
 grep -v "^--$" |\
 awk -F "\t" '{OFS=","}{print $1,$2,$3,$4,$5, $6, $7, $8, $9}' > ${miranda_csv_file}

echo "${miranda_csv_file} made"

exit
