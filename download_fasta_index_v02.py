#!/usr/bin/enu python

#Atlas Khan
import os 
import sys
import argparse

prog_name = 'download_fasta_index_v02.py'


def main():



    parser = argparse.ArgumentParser(description='Downloaded the fasta file and generate the index file', prog = prog_name)

    parser.add_argument('-buildver', '--hg',  required = True, metavar = 'The genome version', type = str, help ='The version of the genome')


    args = parser.parse_args()
    hg=args.hg

    os.system('''mkdir -p  human_reference''')

    def download_fasta():

        if (hg=="hg38"):
            print ("---------------------------------------- The downloading the hg38 fasta file from gencode -----------------------------------------------------")
            os.system('''wget ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_27/GRCh38.p10.genome.fa.gz -P human_reference''')
    
            print ("---------------------------------------- The downloading the gtf file from gencode -----------------------------------------------------")
            os.system('''wget human_reference/ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_27/gencode.v27.chr_patch_hapl_scaff.annotation.gtf.gz -P human_reference''')
    
            os.system('''gunzip  human_reference/GRCh38.p10.genome.fa.gz''')
            os.system('''gunzip human_reference/gencode.v27.chr_patch_hapl_scaff.annotation.gtf.gz''')

   
            print ("---------------------------------------- Generating the index file by using bowte 2 -----------------------------------------------------")

            os.system('''bowtie2-build human_reference/GRCh38.p10.genome.fa human_reference/GRCh38.p10.genome''') 


        elif (hg=="hg19"):
            print ("---------------------------------------- The downloading the hg19 fasta file from gencode -----------------------------------------------------")
            os.system('''wget ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_27/GRCh37_mapping/GRCh37.primary_assembly.genome.fa.gz -P human_reference''')

            print ("---------------------------------------- The downloading the gtf file from gencode -----------------------------------------------------")
            os.system('''wget ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_27/GRCh37_mapping/gencode.v27lift37.annotation.gtf.gz -P human_reference''')

            os.system('''gunzip  human_reference/GRCh37.primary_assembly.genome.fa.gz''')
            os.system('''gunzip human_reference/GRCh37_mapping/gencode.v27lift37.annotation.gtf.gz''')


            print ("---------------------------------------- Generating the index file by using bowte 2 -----------------------------------------------------")

            os.system('''bowtie2-build human_reference/GRCh38.p10.genome.fa human_reference/GRCh38.p10.genome''')



    download_fasta()


if __name__ == '__main__':
    main()


