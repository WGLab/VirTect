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

prog="VerTect.py"


version = """%prog
Copyright (C) 2017 Wang Genomic Lab
VerTect is free for non-commercial use without warranty.
Please contact the authors for commercial use.
Written by Atlas Khan ,ak4046@cumc.columbia.edu and atlas.akhan@gmail.com.
============================================================================
"""

usage = """Usage: %prog[-h] -1 read1.fastq -2 read2.fastq -o The output name for
                  alignement -ucsc_gene gtf -index index files -index_vir
                  virus fasta [-t Number of threads, default: 8]"""




def main():

    parser = argparse.ArgumentParser(description='VirTect: A pipeline for Virus detection')

    parser.add_argument('-1', '--fq1',  required = True, metavar = 'read1.fastq', type = str, help ='The read 1 of the paired end RNA-seq')
 
    parser.add_argument('-2', '--fq2',  required = True, metavar = 'read2.fastq', type = str, help ='The read 2 of the paired end RNA-seq')

    parser.add_argument('-o', '--out',  required = True, metavar = 'The output name for alignement', type = str, help ='Define the output directory to be stored the alignement results')

    parser.add_argument('-ucsc_gene', '--gtf',  required = True, metavar = 'gtf', type = str, help ='The input gtf file')

    parser.add_argument('-index', '--index_dir',  required = True, metavar = 'index files', type = str, help ='The directory of index files with hg38 prefix of the fasta file i.e,. index_files_directory/hg38')

    parser.add_argument('-index_vir', '--index_vir',  required = True, metavar = 'virus fasta', type = str, help ='The fasta file of the virus genomes')

    parser.add_argument('-t', '--n_thread', required = False, metavar = 'Number of threads, default: 8', default = '8', type = str, help ='Number of threads')

    args = parser.parse_args()
    
    fq1 = os.path.abspath(args.fq1)
    
    fq2 = os.path.abspath(args.fq2)
   


    out = os.path.abspath(args.out)
    
    gtf = os.path.abspath(args.gtf)
    

    index_dir = os.path.abspath(args.index_dir)
    
    
    index_vir = os.path.abspath(args.index_vir)
    
    n_thread = args.n_thread


    print ("Aligning by tophat")
    def alignment():
        cmd1='tophat -o '+out+' -p '+n_thread+' -G '+gtf+' '+index_dir+' '+fq1+'  '+fq2+''
        print 'Running ', cmd1
        os.system(cmd1)
    alignment()
        
    def bam2fastq():
        cmd2 ='samtools sort -n  '+out+'/unmapped.bam  -o '+out+'_sorted.bam' 
        print 'Running ', cmd2
        os.system(cmd2)    
        cmd3='bedtools bamtofastq -i  '+out+'_sorted.bam -fq  '+out+'_sorted_1.fq -fq2  '+out+'_sorted_2.fq'    
        print 'Running ', cmd3
        os.system(cmd3)
    bam2fastq()
 
    def bwa_alignment():
        cmd4= 'bwa mem '+index_vir+'  '+out+'_sorted_1.fq '+out+'_sorted_2.fq > '+out+'_aln.sam'
        print 'Running ', cmd4
        os.system(cmd4)
    bwa_alignment()
    
    def virus_detection():
        cmd5= 'samtools view -Sb -h '+out+'_aln.sam > '+out+'_aln.bam'
        print 'Running ', cmd5
        os.system(cmd5)

        cmd6= '''samtools view '''+out+"_aln.bam"+''' | cut -f3 | sort | uniq -c | awk '{if ($1>=400) print $0}' > '''+out+"_viruses_count.txt"+''' '''
        print 'Running ', cmd6
        os.system(cmd6)
    virus_detection() 
        
    def sort():
        cmd7= '''samtools sort '''+out+"_aln.bam"+'''  -o '''+out+"_aln_sorted.bam"+''' '''
        os.system(cmd7)
    sort()
    
    subprocess.call("./continuous_region.sh", shell=True)

    
    print ("The continous length")
    file =open("continuous_region.txt", "r")

    out =open("Final_continous_region.txt", "w")
    
    if (os.fstat(file.fileno()).st_size) >0:
            for i in file.readlines():
                i1=i.split()[0]
                i2=i.split()[1]
                j1=i2.split("-")
                j2=int(j1[1])-int(j1[0])


                if j2 >= 100:
                    j3=i1 + "\t" +  str(j1[0]) + '\t' +  str(j1[1])
                    out.write('%s\n' % j3)
                   
                else:
                    pass                   
    else:
        pass 
    out.close()
    

    final_output=open("Final_continous_region.txt")
    if (os.fstat(final_output.fileno()).st_size) >0:
        print ("----------------------------------------Note: The sample may have some real virus in the sample :(-----------------------------------------------------")
        headers = 'virus transcript_start transcript_end'.split()
        for line in fileinput.input(['Final_continous_region.txt'], inplace=True):
            if fileinput.isfirstline():
                print '\t'.join(headers)
            print line.strip()
    else:
        print ("----------------------------------------Note: There is no real virus in the sample :)-----------------------------------------------------")

if __name__ == '__main__':
    main()
 




