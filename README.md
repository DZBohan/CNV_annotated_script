# CNV Annotated Script 

## 1. Introduction

This CNV annotated script is a python program that can be used along with the CNV analysis pipelines to convert the results from segment-level to other more specific levels, such as gene-level and exon-level, and make the results more apparent.

Most CNV analysis pipelines, such as [GATK](https://github.com/DZBohan/GATK_CNV_Pipeline.git) and [sequenza](https://github.com/DZBohan/Sequenza_Pipeline.git) CNV pipelines, usually divide chromosomes into segments depending on the copy number variation. However, in a real-life scenario, people prefer to know the CNV of some meaningful segments like genes and exons rather than segments divided by algorithm. In this documentation, I will use `gene` standing for all types of meaningful segments, but you should know that the results of this program are not limited to the gene level.

`Log2 copy ratio` is often used to represent changes in segments' copy numbers, but it does not give an excellent visual indication of segments' copy number loss or gain. With this script, you can set lower and upper thresholds for segments' copy number loss and gain to visualize the change in copy number for each gene.

## 2. Standard Input Files

This CNV annotated script should have two input files. The first one is the output segment-level CNV results from CNV pipelines. The second one is a geneinfo file containing all human genes and their position on chromosomes.

The segment-level CNV files should be like this.

![SEGIMAGE](https://github.com/DZBohan/CNV_annotated_script/blob/main/images/segfile_sample_2.png?raw=true)

A CNV pipeline can generate the segment-level CNV input table.

There are four columns in this table. Each row of the table stands for a segment distinguished by the algorithm of the CNV pipeline. The first three columns of the table, `Chromosome`, `Start`, and `End`, give the positions of segments. 

The last column, `Segment_Mean`, means the CNV of a segment. We recommend you use `log2 copy ratio` to represent the CNV.

The geneinfo file includes five columns. You can use the GRCh38 geneinfo file we provide in most cases, but you can also use other versions. Make sure the column names are the same as the ones in the geneinfo file we provide, and the chromosome numbers column in this file has a different format from the segment-level CNV file, which does not have 'chr'.

![GENEIUNFO](https://github.com/DZBohan/CNV_annotated_script/blob/main/images/geneinfo_file.png?raw=true)

In addition, this file is not limited to information about genes. You can also use exome, transcriptome, and other information with the same format to generate other levels of CNV results.

## 3. Algorithm

The basic algorithm of this script is to align genomic genes to segments in the segment-level CNV table and assign the log2 copy rate of the segments to the aligned genes.

![Algorithm](https://github.com/DZBohan/CNV_annotated_script/blob/main/images/alg.png?raw=true)

The figure above shows the simplest alignment case, but more complex cases arise during the alignment process.

When aligning genomic genes to segments in the segment-level CNV table to obtain gene-level CNV, four scenarios will be encountered during the alignment process.

![Overlap](https://github.com/DZBohan/CNV_annotated_script/blob/main/images/overlap.png?raw=true)

For a gene, the first case is that no segment overlaps it. This case is more common at the beginning and end of a chromosome; the gene may also be located in the gap between two segments. For this case, we mark the gene as no_overlap.

The second scenario is that the gene only overlaps with one segment, which is the most common case. For this scenario, the CNV of the gene is assigned a log2 copy rate of this segment.

The third case is that the gene overlaps with two segments. The fourth case is that the gene overlaps with more than two segments. For both cases, we take the maximum value of the absolute value of the `log2 copy ratio` of these segments that have overlap with the gene as the CNV of the gene. Here is an example of assigning log2 copy ratio from segments to genes.

![value](https://github.com/DZBohan/CNV_annotated_script/blob/main/images/value.png?raw=true)

After assigning the corresponding log2 copy ratio to all genes, we assign them the more intuitive CNV expressions, `loss`, `gain` or `normal`. When using the script, you need to enter three threshold parameters for determining the CNV of genes, `--upper`, `--lower` and `--segmax`.

![Threshold](https://github.com/DZBohan/CNV_annotated_script/blob/main/images/thres.png?raw=true)

A gene with a log2 copy ratio greater than the `--upper` argument and the length of the original segment given its log2 copy ratio is less than or equal to `--segmax` is defined as a copy number `gain`; similarly, a gene with a log2 copy ratoo less than the `--lower` argument and the length of the original segment given its log2 copy rate is less than or equal to `--segmax` is defined as a copy number `loss`. A gene with a log2 copy ratio between `--upper` and `--lower` or with the length of the original fragment given its log2 copy rate greater than `--segmax` is defined as `normal`.

## 4. How To Use

Using this annotation script, you can run it by Python3 with seven parameters. Let's have a look at them.

* `-U` or `--upper`: upper threshold of normal copy number. Copy numbers higher than this value should be defined as copy gain (default = 0.58)
* `-L` or `--lower`: lower threshold of normal copy number. Copy numbers lower than this value should be defined as copy loss (default = -1)
* `-M` or `--segmax`: maximum length of segments being used (default = 25000000)
* `-O` or `--outpath`: full path of the directory to store the results (default = current path)
* `-N` or `--name`: name of the sample (no default)
* `-G` or `--geneinfo`: full path of the geneinfo file (no default)
* `-S` or `--segfile`: full path of the segment-level CNV file (no default)

Here are some examples of using this annotated script in the terminal.

```
python3 CNV_annotation_script.py -N sample1 -G geneInfo_GRCh38.txt -S sample1.seg 
```

If you run the program using the above command, the upper threshold, lower threshold, and segment longest threshold will take the default values, and the results will be output to the current path.

```
python3 CNV_annotation_script.py -N sample1 -U 0.3 -L -0.3 -M 30000000 -G geneInfo_GRCh38.txt -S sample1.seg -O /Users/username/Documents/
```

If you run the program using the above command, the upper threshold will be set as 0.3, the lower threshold will be set as -0.3, the segment longest threshold will be set as 30000000, and the results will be output to the path you choose.

You would end up with two tables. The first table, `sample_annotation.txt`, contains all the genes in the genome, their `log2 copy ratio` and their `copy number variations`. There are four types of genes, `no_overlap`, `normal`, `loss` and `gain`. `no_overlap` means that there is no overlap with the gene in the original segment-level CNV table. `normal` means that there is no change in the copy number of the gene. `loss` and `gain` means that there is copy loss and gain of the gene, respectively. The second table, `sample_annotation_report.txt`, contains only information about the genes with copy loss and gain.


This is an example of a final output table, `sample_annotation.txt`.

![fullres](https://github.com/DZBohan/CNV_annotated_script/blob/main/images/fullres.png?raw=true)

This is an example of a final output table, `sample_annotation_report.txt`.

![report](https://github.com/DZBohan/CNV_annotated_script/blob/main/images/report.png?raw=true)