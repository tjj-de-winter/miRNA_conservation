# extract the full mouse Cmtm6 3'UTR into a FASTA file

gtf=mouse_genome/Mus_musculus.GRCm39.113.gtf.gz
fasta=mouse_genome/Mus_musculus.GRCm39.dna.chromosome.9.fa

name="mouse_Cmtm6"
gene_symbol="Cmtm6"

gtf_cmtm6=${name}.gtf

gzcat $gtf | grep $gene_symbol > $gtf_cmtm6

gtf=$gtf_cmtm6

#for 3'UTR
start=$(grep "three_prime_utr" $gtf | awk -F"\t" '{print $4}')
stop=$(grep "three_prime_utr" $gtf | awk -F"\t" '{print $5}')
chromosome=$(grep "three_prime_utr" $gtf | awk -F"\t" '{print $1}')
orientation=$(grep "three_prime_utr" $gtf | awk -F"\t" '{print $7}')

bed=${name}.bed

echo "${chromosome}\t${start}\t${stop}\t${name}_3UTR\t.\t${orientation}"  > $bed

echo "bed file made"

fasta_out=${name}.fasta

bedtools getfasta -fi $fasta -fo $fasta_out -bed $bed -name -s

echo "fasta file made"
