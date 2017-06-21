#!/usr/bin/env python
# Atlas Khan

#05/31/2017

import sys, argparse, os

def main():
    parser = argparse.ArgumentParser(description='VirTect: Pipeline for Virus detection')
    parser.add_argument('-1', '--fq1',  required = True, metavar = 'read1.fastq', type = str, help ='read1.fastq')
    parser.add_argument('-2', '--fq2',  required = True, metavar = 'read2.fastq', type = str, help ='read2.fastq')
    parser.add_argument('-o', '--out_dir',  required = True, metavar = 'output directory', type = str, help ='output directory')
    parser.add_argument('-ucsc_gene', '--gtf',  required = True, metavar = 'Reference', type = str, help ='Reference and index files')
    parser.add_argument('-index', '--index_dir',  required = True, metavar = 'index files directory', type = str, help ='Reference and index files')
    parser.add_argument('-index_vir', '--index_vir',  required = True, metavar = 'index files directory', type = str, help ='Reference and index files')
    parser.add_argument('-t', '--n_thread', required = False, metavar = 'number of threads, default: 12', default = '8', type = str, help ='number of threads')

    args = parser.parse_args()
    fq1 = os.path.abspath(args.fq1)
    fq2 = os.path.abspath(args.fq2)
    out_dir = os.path.abspath(args.out_dir)
    gtf = os.path.abspath(args.gtf)
    index_dir = os.path.abspath(args.index_dir)
    index_vir = os.path.abspath(args.index_vir)
    n_thread = args.n_thread

    #if (args.sample_name):
     #   sample_name = args.sample_name
    #else:
     #   fq1_name = os.path.split(fq1)[1]
     #   sample = fq1_name.split('_')[0]
   
    #cmd = 'mkdir -p '+out_dir+'_aln'
    
    #os.system(cmd)
    #cmd =  ''+out_dir+'_aln' 

    #os.system(cmd)
    

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
        cmd4= 'bwa mem '+index_vir+'  '+out_dir+'_sorted_1.fq '+out_dir+'_sorted_2.fq > aln_'+out_dir+'.sam'
        print 'Running ', cmd4
        os.system(cmd4)
    bwa_alignment()
    
    def virus_detection():
        cmd5= 'samtools view -Sb -h aln_'+out_dir+'.sam > aln_'+out_dir+'.bam'
        print 'Running ', cmd5
        os.system(cmd5)

        cmd6= '''samtools view aln_'+out_dir+'.bam | cut -f3 | sort | uniq -c | awk '{if ($1>=400) print $0}' > '+out_dir+'.viruses_count.txt'''
        print 'Running ', cmd6
        os.system(cmd6)
    virus_detection() 
    
    def continuous_region(coverage):
        cmd7= '''samtools depth aln_'+out_dir+'.bam | awk '{if ($3>=+coverage+) print $0}' | awk '{ if ($2!=(ploc+1)) {if (ploc!=0){printf("%s %d-%d\n",$1,s,ploc);}s=$2} ploc=$2; }' > Continuous_virus.txt'''
        print 'Running ', cmd7
        os.system(cmd7)
    continuous_region()



if __name__ == '__main__':
    main()

