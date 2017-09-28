##################################################################################
# Author: Atlas Khan (ak4046@cumc.columbia.edu)
# Created Time: 2017-05-31
# Wang genomics lab http://wglab.org/
# Description: python script for trimming of RNA-seq data using cutadapt 
##################################################################################

#!/usr/bin/env python

import sys
import argparse
import os
import subprocess
import os.path

prog="cutadapt.py"


version = """%prog
Copyright (C) 2017 Wang Genomic Lab
VerTect is free for non-commercial use without warranty.
Please contact the authors for commercial use.
Written by Atlas Khan, ak4046@cumc.columbia.edu and atlas.akhan@gmail.com.
============================================================================
"""

usage = """usage: cutadapt.py [-h] -1 read1.fastq -2 read2.fastq -F adapt1 -R adapt2"""



def main():

    parser = argparse.ArgumentParser(description='Trimming of RNA-seq data')
    parser.add_argument('-1', '--fq1',  required = True, metavar = 'read1.fastq', type = str, help ='The read 1 of the paired end RNA-seq')
    parser.add_argument('-2', '--fq2',  required = True, metavar = 'read2.fastq', type = str, help ='The read 2 of the paired end RNA-seq')
    

    parser.add_argument('-F', '--adapt1',  required = True, metavar = 'adapt1', type = str, help ='The forward adapter')
    parser.add_argument('-R', '--adapt2',  required = True, metavar = 'adapt2', type = str, help ='The reverse adapter')

    args = parser.parse_args()
    fq1 = os.path.abspath(args.fq1)
    fq2 = os.path.abspath(args.fq2)

    adapt1 = args.adapt1
    adapt2 = args.adapt2

  


    try:
        #f1=open(fq1,'r')
        os.path.isfile(fq1)
        f1=open(fq1,'r')

    except IOError:
        print('Error: There was no Read 1 FASTQ file!')
        sys.exit()


    fq2 = os.path.abspath(args.fq2)


    try:
        #os.path.isfile(fq2)
        f2=open(fq2,'r')

    except IOError:

        print('Error: There was no Read 2 FASTQ file!')
        sys.exit()

    os.system('''mkdir -p trimmed_data''')
    sample1=fq1.split('.')[0]
    sample2=fq2.split('.')[0]


    os.system('''~/.local/bin/cutadapt -a '''+ adapt1 +''' -A '''+ adapt2 +''' -m 40 -q 20,20 -o sample1'''+'''"_trimmed_1.fq" -p sample2'''+'''"_trimmed_2.fq" '''+fq1+''' '''+ fq2 +'''''') 


if __name__ == '__main__':
    main()

