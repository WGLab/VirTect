## VirTect


VirTect is a software tool that detect virus from RNA-Seq on human samples.


## Introduction

VirTect is an efficient software tool for virus detection. VirTect take NGS data as a input in FASTQ format and mapped to human reference genome using tophat. After subtraction of non-human sequence from the human sequence, VirTect used bwa-men command to align the non-human sequence to our defined 757 different viruses database to report the virus. After alignment of non-human sequence to virus database, VirTect do the filtrations to discriminate the viral sequence from the noise or artifact and finally report the real viruses. 

Here is an example that how VirTect works, for the HCC sample, we have about 53 million paired reads, VirTect mapped about 51 of 53 million reads (about 96.7%) to human reference and subtracted the remaining about 2 millions, the non-human reads from the human sequence. Then VirTect mapped the non-human sequence to virues geomes, before filtrations, thousands of reads are mapped to different viruses in our defined virus database such as mapped to tick borne encephalitis, hepatitis C, cutthroat trout, and hepatitis B etc., however, only hepatitis B passed VirTect filtrations. Also we examined some of the virus, which did not pass our filtrations, however significant number of non-human reads mapped to them and we found that it is not a real viral sequence, however, it is mapped to poly(A) sequence of hepatitis C genotype 1.


This is the GitHub repository for the documentation of the VirTect software, described in the paper listed below. If you like this repository, please click on the "Star" button on top of this page, to show appreciation to the repository maintainer. If you want to receive notifications on changes to this repository, please click the "Watch" button on top of this page.

## Dependency

First we need to install the following publicly available tools to run the VirTect:

cutadapt (http://cutadapt.readthedocs.io/en/stable/guide.html)

tophat (https://ccb.jhu.edu/software/tophat/index.shtml)

bwa (http://bio-bwa.sourceforge.net/bwa.shtml)

bowtie2 (http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)

samtools (http://samtools.sourceforge.net/)

bedtools (http://bedtools.readthedocs.io/en/latest/)

FASTQC (https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)

IGV (http://software.broadinstitute.org/software/igv/)

DAVID (https://david.ncifcrf.gov/)

## Links of useful database

TCGA (https://cancergenome.nih.gov/)

Human Papillomavirus (HPV) (https://pave.niaid.nih.gov/#home)



## Installation

Please clone the repository into your computer:

    git clone https://github.com/WGLab/VirTect

Then enter VirTect directory:

    cd VirTect
    
## Trimming

Before, we use VerTict, we need to trim the data to make sure the quality of the data. To trim the data, we need to use the following code to trim the data, if you already trim the data, then no need to do the trimming again.

    python VerTect_cutadapt.py --help
    
    python VerTect_cutadapt.py -1 Reads_1.fq -2 Reads_2.fq -F "AGATCGGAAGAG" -R "AGATCGGAAGAG"


Here -F and -R are forward standard and reverse adapters, however, you may change them if your adapter is different.

## Download and generate the index of human fasta file

Firsrt need to download the fasta file, if you don't have the human fasta file, however, only run this code for first time to download the fasta file and geneate the index for fasta file.

    python download_fasta_index_v02.py --help
    
    python download_fasta_index_v02.py -buildver hg38/hg19  
    
This will downlaod the fasta, the gencode gtf files, and also will generate the index file and will save in human_reference directory **this should be run for first time**. It will download the hg38 or hg19 fasta file based on user input i.e., if you want to download hg38 fasta file then the command will be: *python download_fasta_index_v02.py -buildver hg38* and same for hg19.

## Viruses reference genomes

We already download and generate the index for each of the virus in our virus database, which are saved in viruses_reference directory, which can be used directly from this directory.  

## Synopsis

Fianly run the VirTect for virus detection from human RNA-seq data.

## OPTIONS
 
 * -h, --help            show this help message and exit
 * --version show program''s version number and exit
 
 * -t Number of threads, default: 8, --n_thread Number of threads, default: 8
                        Number of threads
 * -1 read1.fastq, --fq1 read1.fastq
                        The read 1 of the paired end RNA-seq
 * -2 read2.fastq, --fq2 read2.fastq
                        The read 2 of the paired end RNA-seq
 * -o The output name for alignement, --out The output name for alignement
                        Define the output directory to be stored the
                        alignement results
 * -ucsc_gene gtf, --gtf gtf
                        The input gtf file
 * -index index files, --index_dir index files
                        The directory of index files with hg38 prefix of the
                        fasta file i.e,. index_files_directory/hg38
 * -index_vir virus fasta, --index_vir virus fasta
                        The fasta file of the virus genomes
 * -d continuous_distance, --distance continuous_distance
                        Define the continuous mapping distance of mapping
                        reads to virus genome

## Example

    python VirTect.py --help
    
    python VirTect.py -t 12 -1 Reads_1.fq -2 Reads_2.fq -o Test -ucsc_gene human_reference/gencode.v25.chr_patch_hapl_scaff.annotation.gtf -index human_reference/GRCh38.p10.genome -index_vir viruses_reference/viruses_757.fasta -d 200

After the running VerTect, we will have the final viruses file *Final_continous_region.txt*, if the sample has some virus/viruses. The continuous distance mapping distance virus genome depends on user input lenght of reads. 

## Virus expression count

After virus detection from the samples, we may need to know that which gene is expressed in specfic virus, we need to do the Virus expression count. We need to run the following code to generate the count file. We have only viurs annotations for some HPV virus, however, we will work on it provide the annotation file for each of the virus in our virus database.

    python VerTect_count_expression.py --help

Still we are working on it to provide annotations for each of the virus in our virus database.


## License Agreement

By using the software, you acknowledge that you agree to the terms below:

For academic and non-profit use, you fell free to fork, download, modify, distribute and use the software without restriction.
 
 ## Contact
Atlas Khan (ak4046@cumc.columbia.edu)

Kai Wang (kw2701@cumc.columbia.edu)

## Reference

Khan A, Stucky A, Parish P. Sedghizadeh, Daniel A, Zhang Xi, Wang K, Zhong JF, **A viral genome detection method reveals HPV carcinogenesis mechanism in head and neck squamous cell carcinoma**, Submitted. 


## More information
Wang Genomics Lab Homepage (http://wglab.org/)
