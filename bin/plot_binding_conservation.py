import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import psa
import fastapy
import re
from pygenomeviz import GenomeViz

# functions

def get_species(string):
    if 'human' in string:
        return 'human'
    elif 'mouse' in string:
        return 'mouse'
    else:
        return 'rat'

def get_colors_cmap(values, label):
    '''Extract colormap HEX values from a list of values and generate a colormap'''
    # Normalize values between 0 and 1
    norm = plt.Normalize(min(values), max(values))

    # Get viridis colormap
    colormap = plt.cm.viridis

    # Get color codes
    colors = [colormap(norm(v)) for v in values]

    # Convert RGBA to HEX
    hex_colors = [mcolors.rgb2hex(c[:3]) for c in colors]
    
    # Create a figure without an axis
    fig, ax = plt.subplots(figsize=(6, 1), dpi=300)
    fig.patch.set_visible(False)  # Hide figure background
    ax.axis("off")  # Remove axes

    # Create ScalarMappable for the colorbar
    sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=norm)
    sm.set_array([])  # Dummy array for colorbar

    # Add colorbar
    cbar = plt.colorbar(sm, orientation='horizontal', ax=ax)
    cbar.set_label("label")

    plt.savefig(f'./colorbar_{label}.pdf')

    return hex_colors

def find_sequence_indices(large_seq, small_seq):
    # Escape any special characters in the small sequence (not needed for standard nucleotides)
    pattern = re.compile(small_seq)

    # Find all matches
    matches = [(match.start(), match.group()) for match in pattern.finditer(large_seq)]

    return matches

def get_links(species1, species2, name_dict):
    aln = psa.needle(moltype='nucl',
                     qseq=seq_dict[species1],
                     sseq=seq_dict[species2],
                     qid=species1,
                     sid=species2)

    # find the sequneces with matching overlap
    matching_seqs_1 = []
    matching_seqs_2 = []
    s1 = ''
    s2 = ''

    for n1, n2 in aln:
        if n1 == n2:
        # if n1 != '-' and n2 != '-':
            s1 += n1
            s2 += n2
        else:
            if s1 != '':
                matching_seqs_1.append(s1)
                matching_seqs_2.append(s2)
                s1 = ''
                s2 = ''

    species1_links = []
    current_index = 0
    for match in matching_seqs_1:
        matches = find_sequence_indices(seq_dict[species1][current_index:], match)
        first_match = matches[0]

        start = first_match[0]+current_index
        stop = start + len(first_match[1])

        current_index = stop

        species1_links.append((name_dict[species1], start, stop))
        
    return species1_links

### load miranda results file (generate by ./miranda.sh)

file = './miranda/CMTM6_hsa-miR-642.miranda.out.csv'

df = pd.read_csv(file, sep=',',names=['mirna','Target','Score','Energy-Kcal/Mol','Query-Aln(start-end)','Subjetct-Al(Start-End)','Al-Len','Subject-Identity','Query-Identity'])

df['mirna'] = [i.strip('>') for i in df['mirna']] 
    
df['Species'] = [get_species(i) for i in df['Target']] 
df['start'] = [int(i.split(' ')[0]) for i in df['Subjetct-Al(Start-End)']]
df['stop'] = [int(i.split(' ')[1]) for i in df['Subjetct-Al(Start-End)']]

df_all = df.copy()

### plot the miRNA binding sites for hsa-miR-642a-3p
species_list = ['mouse', 'rat','human']
gene = {'human':"CMTM6 3'UTR", 'rat':"Cmtm6 3'UTR", 'mouse':"Cmtm6 3'UTR"}
mirna = 'hsa-miR-642a-3p'

start = df_all['start'].min()
stop = df_all['stop'].max()

gv = GenomeViz()
gv.set_scale_xticks(ymargin=0.5)

scores = list(df_all[(df_all['mirna'] == mirna)]['Score'])
colors = get_colors_cmap(scores, mirna)
color_dict = {score: color for score, color in zip(scores, colors)}

for xi, species in enumerate(species_list):
    df = df_all[df_all['Species'] == species].copy()
        
    target = list(df['Target'])[0]
    target = target.rsplit('::')[1].rsplit('(')[0].rsplit(':')[1].rsplit('-')
    target = [int(t) for t in target]
    gene_start, gene_stop = target
    length = abs(gene_start -  gene_stop)
    df_match = df[(df_all['mirna'] == mirna)]
    
    track = gv.add_feature_track(' '.join([species, gene[species]]), length)
    track.add_sublabel()
    
    for i, idx in enumerate(df_match.index):
        start_ = int(df_match.loc[idx,'start'])
        stop_ = int(df_match.loc[idx,'stop'])
        score_ = df_match.loc[idx,'Score']
        track.add_feature(start_, start_+20, 1, fc=color_dict[score_])

### add sequence conservation to plot

fasta = 'CMTM6_seqs.fasta'
seq_dict = {}
for record in fastapy.parse(fasta):
    seq_dict[record.id.split('_')[0]] = record.seq

name_dict = gene = {'human':"human CMTM6 3'UTR", 'rat':"rat Cmtm6 3'UTR", 'mouse':"mouse Cmtm6 3'UTR"}

links1 = get_links('rat', 'human', name_dict)
links2 = get_links('human', 'rat', name_dict)
links3 = get_links('rat', 'mouse', name_dict)
links4 = get_links('mouse', 'rat', name_dict)

print(links1)
for link1, link2 in zip(links1, links2): 
    gv.add_link(link1, link2, curve=True) # human vs rat
    
for link3, link4 in zip(links3, links4): 
    gv.add_link(link3, link4, curve=True) # mouse vs rat


gv.savefig(f"{mirna}_CMTM6_species.png")

### plot the miRNA binding sites for hsa-miR-642b-3p
species_list = ['mouse', 'rat','human']
gene = {'human':"CMTM6 3'UTR", 'rat':"Cmtm6 3'UTR", 'mouse':"Cmtm6 3'UTR"}
mirna = 'hsa-miR-642b-3p'

start = df_all['start'].min()
stop = df_all['stop'].max()

gv = GenomeViz()
gv.set_scale_xticks(ymargin=0.5)

scores = list(df_all[(df_all['mirna'] == mirna)]['Score'])
colors = get_colors_cmap(scores, mirna)
color_dict = {score: color for score, color in zip(scores, colors)}

for xi, species in enumerate(species_list):
    df = df_all[df_all['Species'] == species].copy()
        
    target = list(df['Target'])[0]
    target = target.rsplit('::')[1].rsplit('(')[0].rsplit(':')[1].rsplit('-')
    target = [int(t) for t in target]
    gene_start, gene_stop = target
    length = abs(gene_start -  gene_stop)
    df_match = df[(df_all['mirna'] == mirna)]
    
    track = gv.add_feature_track(' '.join([species, gene[species]]), length)
    track.add_sublabel()
    
    for i, idx in enumerate(df_match.index):
        start_ = int(df_match.loc[idx,'start'])
        stop_ = int(df_match.loc[idx,'stop'])
        score_ = df_match.loc[idx,'Score']
        track.add_feature(start_, start_+20, 1, fc=color_dict[score_])

### add sequence conservation to plot

fasta = 'CMTM6_seqs.fasta'
seq_dict = {}
for record in fastapy.parse(fasta):
    seq_dict[record.id.split('_')[0]] = record.seq

name_dict = gene = {'human':"human CMTM6 3'UTR", 'rat':"rat Cmtm6 3'UTR", 'mouse':"mouse Cmtm6 3'UTR"}

links1 = get_links('rat', 'human', name_dict)
links2 = get_links('human', 'rat', name_dict)
links3 = get_links('rat', 'mouse', name_dict)
links4 = get_links('mouse', 'rat', name_dict)

print(links1)
for link1, link2 in zip(links1, links2): 
    gv.add_link(link1, link2, curve=True) # human vs rat
    
for link3, link4 in zip(links3, links4): 
    gv.add_link(link3, link4, curve=True) # mouse vs rat


gv.savefig(f"{mirna}_CMTM6_species.png")
