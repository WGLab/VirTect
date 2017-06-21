VirTect


Virtect is a softare that detected virus from from RNA-Seq on human samples.


Introduction

VirTect is an efficient software tool for virus detection. Virtect take NGS data as a input in FASTQ format and mapped to human reference genome using tophat. After subtraction of non-human sequence from the human sequence, VirTecst used bwa-men command to align the non-human sequence to our defined 757 different virus database to report the virus. After alignment of non-human sequence to virus database, VirTect do the filtrations to discriminate the viral sequence from the noise/artifact and finally report the viruses. 

Here is an example that how VirTect works, for the HCC sample, we have about 53 million paired reads,. VirTect mapped about 51 of 53 million reads (about 96.7%) to human reference and subtracted the remaining about 2 million, the non-human reads from the human sequence. Before filtrations, thousands of reads are mapped to different viruses in our defined virus database such as aligned to tick borne encephalitis, hepatitis C, cutthroat trout, and hepatitis B etc., however, only hepatitis B passed our filtrations and we examined in IGV to see the coverage in Figure 1. Also we examined some of the virus, which did not pass our filtrations, however significant number of non-human reads mapped to them and we found that it is not a real viral sequence, however, it is mapped to poly(A) sequence of hepatitis C genotype 1.


This is the GitHub repository for the documentation of the VirTect software, described in the paper listed below. If you like this repository, please click on the "Star" button on top of this page, to show appreciation to the repository maintainer. If you want to receive notifications on changes to this repository, please click the "Watch" button on top of this page.

Dependency

tophat (https://ccb.jhu.edu/software/tophat/index.shtml)

samtools (http://samtools.sourceforge.net/)

bedtools (http://bedtools.readthedocs.io/en/latest/)

Installation

Please clone the repository into your computer:

    git clone https://github.com/WGLab/VirTect

Then enter VirTect directory:

    cd VirTect

Synopsis

    python VirTect_v03.py --help

    python VirTect_v03.py -1 Reads_1.fq -2 Reads_2.fq -o Test -ucsc_gene your_file.gtf -index the reference index directory -index_vir The viurs reference file with index -t number of threads


License Agreement

By using the software, you acknowledge that you agree to the terms below:

For academic and non-profit use, you are free to fork, download, modify, distribute and use the software without restriction.
 
 

Reference

Khan A, Stucky A, Wang K, Zhong JF, Zhong, VirTect: Detection of viruses from tumor samples by RNA-Seq, In prepration. 
