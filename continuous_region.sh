#!/bin/bash

for i in *_aln_sorted.bam
do
samtools depth  $i | awk '{if ($3>=5) print $0}' | awk '{ if ($2!=(ploc+1)) {if (ploc!=0){printf("%s %d-%d\n",$1,s,ploc);}s=$2} ploc=$2; }' > continuous_region.txt
done
