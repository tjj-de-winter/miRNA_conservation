![image](https://github.com/user-attachments/assets/814c0b29-92c5-4c08-8c68-c93b1e7f3982)# miRNA_conservation
Here I compute mirna binding conservation for a gene between human, mouse, and rat

### download GTF and FASTA files for each species
<code>./human_genome.sh</code>\
<code>./mouse_genome.sh</code>\
<code>./rat_genome.sh</code>

### Extract 3'UTR sequence and save output as FASTA
<code>./human.sh</code>\
<code>./mouse.sh</code>\
<code>./rat.sh</code>

### Download and Extract sequence of the mature miRNA, using the mirbase database
<code>./mir-642.sh</code>

### Compute miRNA binding scores between 3'UTR and miRNA
<code>./miranda.sh</code>

### Visualize mirna binding and sequence conservation using NEEDLE (EMBOSS) pairwise allignment
<code>./plot_binding_conservation.py</code>

### software requierments
wget (version 1.24.5)\
samtools (version 1.11) https://github.com/samtools/samtools\
bedtools (version v2.30.0) https://github.com/arq5x/bedtools2\
miranda (version v3.3a) https://github.com/hacktrackgnulinux/miranda\
pandas (version 1.5.1) https://github.com/pandas-dev/pandas\
matplotlib (version 3.7.1) https://github.com/matplotlib/matplotlib\
numpy (version 1.23.3) https://github.com/numpy/numpy\
emboss (version 6.6.0.0) https://replikation.github.io/bioinformatics_side/tools/emboss/\
psa (version 1.0.1) https://github.com/aziele/pairwise-sequence-alignment\
fastapy (version 1.0.5) https://github.com/aziele/fastapy\
re (version 2.2.1)\
pygenomeviz (version 1.3.0) https://github.com/moshi4/pyGenomeViz
