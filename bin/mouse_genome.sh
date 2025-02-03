# download and index genome GTF and FASTA

gtf_link="https://ftp.ensembl.org/pub/release-113/gtf/mus_musculus/Mus_musculus.GRCm39.113.gtf.gz"
fasta_link="https://ftp.ensembl.org/pub/release-113/fasta/mus_musculus/dna/Mus_musculus.GRCm39.dna.chromosome.9.fa.gz"

folder=mouse_genome

mkdir -p $folder

cd $folder

# Download GTF file
# wget $gtf_link

# Download FASTA file
# wget $fasta_link

fasta=$(basename $fasta_link)
fasta=${fasta%.gz}

# index FASTA file
gunzip $fasta
samtools faidx $fasta




