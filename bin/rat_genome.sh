gtf_link="https://ftp.ensembl.org/pub/release-113/gtf/rattus_norvegicus/Rattus_norvegicus.mRatBN7.2.113.gtf.gz"
fasta_link="https://ftp.ensembl.org/pub/release-113/fasta/rattus_norvegicus/dna/Rattus_norvegicus.mRatBN7.2.dna.primary_assembly.8.fa.gz"

folder=rat_genome

mkdir -p $folder

cd $folder

# Download GTF file
wget $gtf_link

# Download FASTA file
wget $fasta_link

fasta=$(basename $fasta_link)
fasta=${fasta%.gz}

# index FASTA file
gunzip $fasta
samtools faidx $fasta




