#!/usr/bin/python
import pandas as pd
import sys
import copy

# input parameters
# the path of the standard segment-level CNV table
seg_filename = sys.argv[1]
# the path of the geneinfo table
geneinfo = sys.argv[2]
# type of the segmean value. 3 inputs: cn, cr and log2cr
segmean_type = sys.argv[3]
# sample's name
sample_name = sys.argv[4]

# read the segment-level CNV table and the geneinfo table
gene = pd.read_csv(geneinfo, sep='\t', header=0)
seg = pd.read_csv(seg_filename, sep='\t', header=0)

# add 'chr' into the geneinfo table for the matching
gene['chrom'] = gene['chrom'].map(lambda x: 'chr' + x)

for index, row in gene.iterrows():
    tmp_df = seg.loc[(seg['Chromosome'] == row['chrom']) & (seg['End'] >= row['start']) & (seg['Start'] <= row['end'])]
    # if a gene crosses two segments, it will caculate the mean value of the two segments for that gene
    gene.loc[index,sample_name] = tmp_df['Segment_Mean'].mean()
    # drop the genes in the gap between two segments (have no value)
gene.dropna(axis=0, how='any', inplace=True)

# convert the original indicators into a more direct way showing copy loss or gain
if segmean_type == 'log2cr':
    gene[sample_name] = gene[sample_name].map(lambda x: round(2*(2**x))-2)
elif segmean_type == 'cr':
    gene[sample_name] = gene[sample_name].map(lambda x: round(2*x)-2)
elif segmean_type == 'cn':
    gene[sample_name] = gene[sample_name].map(lambda x: x-2)

# save the final table
gene.to_csv(sample_name + '.txt', sep='\t', index=None)