#!/usr/bin/enu python
#Atlas Khan

import os 
import sys
import argparse

prog_name = 'download_fasta_index_v0.0.2'

def main():



    parser = argparse.ArgumentParser(description='Downloaded the fasta file and generate the index file', prog = prog_name)

    parser.add_argument('-buildver', '--hg',  required = True, default=None, metavar = 'The genome version', type = str, help ='The version of the genome')
    parser.add_argument('-index', '--index',  required = False, default="No", metavar = 'created index file', type = str, help ='Create index file')

    args = parser.parse_args()
    hg=args.hg
    index=args.index

    os.system('''mkdir -p  human_reference''')

    def download_fasta(hg,index):

        if (hg=="hg38"):
            print ("Notice: The downloading the hg38 fasta file from gencode")
            os.system('''wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_29/GRCh38.p12.genome.fa.gz -P human_reference''')
    
            print ("Notice: The downloading the gtf file from gencode")
            os.system('''wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_29/gencode.v29.annotation.gtf.gz -P human_reference''')
            
            print ("Notice: Unziping the gzip files")
            os.system('''gunzip  human_reference/GRCh38.p12.genome.fa.gz''')
            os.system('''gunzip human_reference/gencode.v29.2wayconspseudos.gtf.gz''')

            if (index=="YES"):
                print ("Notice: Generating the index file by using bowte 2")

                os.system('''bowtie2-build human_reference/GRCh38.p12.genome.fa human_reference/GRCh38.p12.genome''')
            else:
                print ("Notice: Only download the fasta and gtf file")    

        elif (hg=="hg19"):
            print ("Notice: The downloading the hg19 fasta file from gencode")
            os.system('''wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_29/GRCh37_mapping/GRCh37.primary_assembly.genome.fa.gz -P human_reference''')

            print ("Notice: The downloading the gtf file from gencode")
            os.system('''wget  ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_29/GRCh37_mapping/gencode.v29lift37.annotation.gtf.gz -P human_reference''')

            print ("Notice: Unziping the gzip files")
            os.system('''gunzip  human_reference/GRCh37.primary_assembly.genome.fa.gz''')
            os.system('''gunzip human_reference/GRCh37_mapping/gencode.v29lift37.annotation.gtf.gz''')


            if (index=="YES"):
                print ("Notice: Generating the index file by using bowte 2")
                os.system('''bowtie2-build human_reference/GRCh37.primary_assembly.genome.fa human_reference/GRCh37.primary_assembly.genome''')
      
            else:
                print ("Notice: Only downloading the fasta and gtf file")
        else:
            print ("Notice: Please choose your fasta file version such as hg19 or hg38")
    download_fasta(hg,index)

if __name__ == '__main__':
    main()
