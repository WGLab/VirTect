#!/usr/bin/env python
# Atlas Khan
# Wang genomics lab http://wglab.org/

#05/31/2017

import sys
import argparse
import os
import subprocess

def main():

    parser = argparse.ArgumentParser(description='VirTect: Pipeline for Virus detection')
    parser.add_argument('-1', '--fq1',  required = True, metavar = 'read1.fastq', type = str, help ='The read 1 of the paired end RNA-seq')
    parser.add_argument('-2', '--fq2',  required = True, metavar = 'read2.fastq', type = str, help ='The read 2 of the paired end RNA-seq')
    parser.add_argument('-o', '--out_dir',  required = True, metavar = 'output directory', type = str, help ='Define the output directory to be stored the alignement results')
    parser.add_argument('-ucsc_gene', '--gtf',  required = True, metavar = 'gtf', type = str, help ='The input gtf file')
    parser.add_argument('-index', '--index_dir',  required = True, metavar = 'index files', type = str, help ='The directory of index files with hg38 prefix of the fasta file i.e,. index_files_directory/hg38')
    parser.add_argument('-index_vir', '--index_vir',  required = True, metavar = 'virus fasta', type = str, help ='The fasta file of the virus genomes')
    parser.add_argument('-t', '--n_thread', required = False, metavar = 'Number of threads, default: 8', default = '8', type = str, help ='Number of threads')

    args = parser.parse_args()
    fq1 = os.path.abspath(args.fq1)
    fq2 = os.path.abspath(args.fq2)
    out_dir = os.path.abspath(args.out_dir)
    gtf = os.path.abspath(args.gtf)
    index_dir = os.path.abspath(args.index_dir)
    index_vir = os.path.abspath(args.index_vir)
    n_thread = args.n_thread


    print ("Aligning by tophat")
    def alignment():
        cmd1='tophat -o '+out_dir+' -p '+n_thread+' -G '+gtf+' '+index_dir+' '+fq1+'  '+fq2+''
        print 'Running ', cmd1
        os.system(cmd1)
    alignment()
        
    def bam2fastq():
        cmd2 ='samtools sort -n  '+out_dir+'/unmapped.bam  -o '+out_dir+'_sorted.bam' 
        print 'Running ', cmd2
        os.system(cmd2)    
        cmd3='bedtools bamtofastq -i  '+out_dir+'_sorted.bam -fq  '+out_dir+'_sorted_1.fq -fq2  '+out_dir+'_sorted_2.fq'    
        print 'Running ', cmd3
        os.system(cmd3)
    bam2fastq()
 
    def bwa_alignment():
        cmd4= 'bwa mem '+index_vir+'  '+out_dir+'_sorted_1.fq '+out_dir+'_sorted_2.fq > '+out_dir+'_aln.sam'
        print 'Running ', cmd4
        os.system(cmd4)
    bwa_alignment()
    
    def virus_detection():
        cmd5= 'samtools view -Sb -h '+out_dir+'_aln.sam > '+out_dir+'_aln.bam'
        print 'Running ', cmd5
        os.system(cmd5)

        cmd6= '''samtools view '''+out_dir+"_aln.bam"+''' | cut -f3 | sort | uniq -c | awk '{if ($1>=400) print $0}' > '''+out_dir+"_viruses_count.txt"+''' '''
        print 'Running ', cmd6
        os.system(cmd6)
    virus_detection() 
        
    def sort():
        cmd7= '''samtools sort '''+out_dir+"_aln.bam"+'''  -o '''+out_dir+"_aln_sorted.bam"+''' '''
        os.system(cmd7)
    sort()
    
    subprocess.call("./continuous_region.sh", shell=True)

    
    print ("The continous length")
    file =open("continuous_region.txt", "r")

    out =open("Final_continous_test_region.txt", "w")
    
    if (os.fstat(file.fileno()).st_size) >0:
            for i in file.readlines():
                i1=i.split()[0]
                i2=i.split()[1]
                j1=i2.split("-")
                j2=int(j1[1])-int(j1[0])


                if j2 >= 100:
                    j3=i1 + "\t" +  str(j1[0]) + '\t' +  str(j1[1])
                    out.write('%s\n' % j3)
                    print ("----------------------------------------The sample may have some real virus in the sample :(-----------------------------------------------------")
                else:
                    print ("----------------------------------------There is no real virus in the sample :)-----------------------------------------------------")
    else:
        print ("----------------------There is no virus at all in the sample :)----------------------------------------------------")
    out.close()
 


if __name__ == '__main__':
    main()
 
