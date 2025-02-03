# download and index genome GTF and FASTA

gtf_link="https://ftp.ensembl.org/pub/release-113/gtf/homo_sapiens/Homo_sapiens.GRCh38.113.gtf.gz"
fasta_link="https://ftp.ensembl.org/pub/release-113/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.3.fa.gz"

folder=human_genome

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
