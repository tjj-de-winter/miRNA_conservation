# extract the full rat Cmtm6 3'UTR into a FASTA file

# to download the files
# ./rat_genome.sh

# input variables:
gtf=rat_genome/Rattus_norvegicus.mRatBN7.2.113.gtf.gz
fasta=rat_genome/Rattus_norvegicus.mRatBN7.2.dna.primary_assembly.8.fa
name="rat_Cmtm6"
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
