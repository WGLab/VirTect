##################################################################################
# Author: Atlas Khan (ak4046@cumc.columbia.edu)
# Created Time: 2017-05-31
# Wang genomics lab http://wglab.org/
# Description: python script for virus detection from human RNA-seq samples
##################################################################################

#!/usr/bin/env python

import sys
import argparse
import os
import subprocess
import os.path
import fileinput

prog="VirTect.py"


version = """%prog
Copyright (C) 2017 Wang Genomic Lab
VerTect is free for non-commercial use without warranty.
Please contact the authors for commercial use.
Written by Atlas Khan, ak4046@cumc.columbia.edu and atlas.akhan@gmail.com.
============================================================================
"""

usage = """Usage: %prog[-h] -1 read1.fastq -2 read2.fastq -o The output name for
                  alignement -ucsc_gene gtf -index index files -index_vir
                  virus fasta [-t Number of threads, default: 8]"""


def main():

    parser = argparse.ArgumentParser(description='VirTect: A pipeline for Virus detection')

    parser.add_argument('-t', '--n_thread', required = False, metavar = 'Number of threads, default: 8', default = '8', type = str, help ='Number of threads') 
    parser.add_argument('-1', '--fq1',  required = True, metavar = 'read1.fastq', type = str, help ='The read 1 of the paired end RNA-seq')
 
    parser.add_argument('-2', '--fq2',  required = True, metavar = 'read2.fastq', type = str, help ='The read 2 of the paired end RNA-seq')

    parser.add_argument('-o', '--out',  required = True, metavar = 'The output name for alignement', type = str, help ='Define the output directory to be stored the alignement results')

    parser.add_argument('-ucsc_gene', '--gtf',  required = True, metavar = 'gtf', type = str, help ='The input gtf file')

    parser.add_argument('-index', '--index_dir',  required = True, metavar = 'index files', type = str, help ='The directory of index files with hg38 prefix of the fasta file i.e,. index_files_directory/hg38')

    parser.add_argument('-index_vir', '--index_vir',  required = True, metavar = 'virus fasta', type = str, help ='The fasta file of the virus genomes')
   
    parser.add_argument('-d', '--distance', required = True, metavar = 'continuous_distance', type = int, help ='Define the continuous mapping distance of mapping reads to virus genome')


    args = parser.parse_args()
    
    fq1 = os.path.abspath(args.fq1)


    try:
        #f1=open(fq1,'r')
        os.path.isfile(fq1)
        f1=open(fq1,'r')
    except IOError:
        print('Error: There was no Read 1 FASTQ file!')
        sys.exit()


    fq2 = os.path.abspath(args.fq2)


    try:
        os.path.isfile(fq2)
        f2=open(fq2,'r')
    
    except IOError:
        print('Error: There was no Read 2 FASTQ file!')
        sys.exit()



    out = os.path.abspath(args.out)
    
 


    gtf = os.path.abspath(args.gtf)
   
    try:
        os.path.isfile(gtf)
        f2=open(gtf,'r')

    except IOError:
        print('Error: There was no GTF file!')
        sys.exit()   

    
    index_dir = os.path.abspath(args.index_dir)

    try:
        os.path.isfile(index_dir)
       # f4=open('hg38'+'."fa"','r')
    except IOError:
        print('Error: There was no fasta index directory!')
        sys.exit()
    
    


    index_vir = os.path.abspath(args.index_vir)

    #try:
     #   os.path.isfile(index_vir)
      #  f4=open(index_vir/viruses_757.fasta,'r')
    #except IOError:
     #   print('Error: There was no virus fasta index directory!')
      #  sys.exit()
    
    n_thread = args.n_thread

    distance = args.distance
    
    
    print ("Aligning by tophat")
    def alignment():
        cmd1='tophat2 -o '+out+' -p '+n_thread+' -G '+gtf+' '+index_dir+' '+fq1+'  '+fq2+''
        print 'Running ', cmd1
        os.system(cmd1)
    alignment()
        
    def bam2fastq():
        cmd2 ='samtools sort -n  '+out+'/unmapped.bam  -o '+out+'/unmapped_sorted.bam' 
        print 'Running ', cmd2
        os.system(cmd2)    
        cmd3='bedtools bamtofastq -i  '+out+'/unmapped_sorted.bam -fq  '+out+'/unmapped_sorted_1.fq -fq2  '+out+'/unmapped_sorted_2.fq'    
        print 'Running ', cmd3
        os.system(cmd3)
    bam2fastq()
 
    def bwa_alignment():
        cmd4= 'bwa mem '+index_vir+'  '+out+'/unmapped_sorted_1.fq '+out+'/unmapped_sorted_2.fq > '+out+'/unmapped_aln.sam'
        print 'Running ', cmd4
        os.system(cmd4)
    bwa_alignment()
    
    def virus_detection():
        cmd5= 'samtools view -Sb -h '+out+'/unmapped_aln.sam > '+out+'/unmapped_aln.bam'
        print 'Running ', cmd5
        os.system(cmd5)

        cmd6= '''samtools view '''+out+"/unmapped_aln.bam"+''' | cut -f3 | sort | uniq -c | awk '{if ($1>=400) print $0}' > '''+out+"/unmapped_viruses_count.txt"+''' '''
        print 'Running ', cmd6
        os.system(cmd6)
    virus_detection() 
        
    def sort():
        cmd7= '''samtools sort '''+out+"/unmapped_aln.bam"+'''  -o '''+out+"/unmapped_aln_sorted.bam"+''' '''
        os.system(cmd7)
    sort()
    
    #
    #subprocess.call("./continuous_region.sh", shell=True)
    os.system('''samtools depth '''+out+"/unmapped_aln_sorted.bam"+''' | awk '{if ($3>=5) print $0}' | awk '{ if ($2!=(ploc+1)) {if (ploc!=0){printf("%s %d-%d\n",$1,s,ploc);}s=$2} ploc=$2; }' > '''+out+"/continuous_region.txt"+'''  ''')
    
    print ("The continous length")
    file =open(out+"/continuous_region.txt", "r")

    out_put =open(out+"/Final_continous_region.txt", "w")
    
    if (os.fstat(file.fileno()).st_size) >0:
            for i in file.readlines():
                i1=i.split()[0]
                i2=i.split()[1]
                j1=i2.split("-")
                j2=int(j1[1])-int(j1[0])


                if j2 >= distance:
                    j3=i1 + "\t" +  str(j1[0]) + '\t' +  str(j1[1])
                    out_put.write('%s\n' % j3)
                   
                else:
                    pass
    else:
        pass 
    out_put.close()
        

    final_output=open(out+"/Final_continous_region.txt",'r')
    if (os.fstat(final_output.fileno()).st_size) >0:
        print ("----------------------------------------Note: The sample may have some real virus :(-----------------------------------------------------")
        headers = 'virus transcript_start transcript_end'.split()
        for line in fileinput.input([out+'/Final_continous_region.txt'], inplace=True):
            if fileinput.isfirstline():
                print '\t'.join(headers)
            print line.strip()
    else:
        print ("----------------------------------------Note: There is no real virus in the sample :)-----------------------------------------------------")

if __name__ == '__main__':
    main()
 




