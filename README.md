# CNV Annotated Script 

## 1. Introduction

This CNV annotated script is a python program that can be used along with the CNV analysis pipelines to convert the results from segments level to genes level and make the results more apparent.

Most CNV analysis pipelines, such as GATK and sequenza CNV pipelines I built before, usually divide chromosomes into segments depending on the copy number variation. However, in real-life scenario, people prefer to know the CNV of genes rather than segments divided by algorithm.

In addition, different CNV analysis tools use different metrics, such as copy number, copy ratio, or log2 copy ratio, to indicate copy number changes, so it is necessary to unify the metrics produced by different tools into the most intuitive ones.

Those are the reasons for developing this CNV annotated program. No matter which CNV analysis tools you use, you will get unified information finally by using the CNV annotated script.

What you get finally is the copy number changes of each gene on different samples of a project. For example, `0` means there is no copy number change, `-1` means there is a copy loss, `1` means there is a copy gain, and `2` means there are two copy gains.

## 2. Standard Input Files

This annotated script should have two input files. The first one is the output segment-level CNV results from CNV pipelines. The second one is a geneinfo file containing all human genes and their position on chromosomes.

The segment-level CNV files should be like this.

![SEGIMAGE](https://github.com/DZBohan/CNV_annotated_script/blob/main/images/segfile_sample.png?raw=true)

There are five columns in the segment-level CNV input table. The first column is supposed to be the samples' names in a specific project. One thing you need to know is that usually, the output table from a CNV pipeline only contains the information of one sample. For example, these are two standard output segment-level CNV tables from the GATK CNV pipeline and sequenza CNV pipeline, respectively.

![GATK](https://github.com/DZBohan/CNV_annotated_script/blob/main/images/example_gatk.png?raw=true)

![SEQUENZA](https://github.com/DZBohan/CNV_annotated_script/blob/main/images/example_sqza.png?raw=true)

Therefore, you can put all segment data from the same project into one table to get a final result of the whole project.

The last column of the segment-level CNV table is called Segment_Mean, meaning a variable that can indicate the copy numbers per segment. In this algorithm, you can use three metrics, copy number, copy ratio, and log2 copy ratio, for this column. 

Different CNV pipelines might use different metrics to indicate copy numbers. GATK CNV pipeline uses log2 copy ratio as the segment mean value, but the sequenza CNV pipeline provides copy number and copy ratio. you can use any of these three metrics to generate the same result.

The geneinfo file also includes five columns. You can use the GRCh38 geneinfo file we provide in most cases, but you can also use your own versions. Make sure the column names are the same as the ones in the geneinfo file we provide, and the chromosome numbers in this file do not have 'chr'.

![GENEIUNFO](https://github.com/DZBohan/CNV_annotated_script/blob/main/images/geneinfo_file.png?raw=true)

In addition, this file is not limited to information about genes. You can also use exome, transcriptome, and other information with the same format to generate other levels of CNV results.

## 3. How To Use

Using this annotation script, you can run it by Python3 with four parameters, the path of the segment-level CNV file, the path of the geneinfo file, the type of the segment mean value you use to indicate the copy number, and the name of the final output file.

As said in the second part, you are allowed to use three types of metrics, `cn`, `cr`, and `log2cr` as the third parameter. `cn` stands for copy number, `cr` stands for copy ratio, and `log2cr` stands for log2 copy ratio.

Here is an example of using this annotated script in the terminal.

```
python3 anno_script.py Sample1.seg GRCh38.txt log2cr project1
```

These are first ten rows of an example of the final output table.

OUTPUT