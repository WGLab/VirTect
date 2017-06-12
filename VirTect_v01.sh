#!/usr/bin/env bash
# M: May 31, 2017
# A: Atlas Khan <atlas.akhan@gmail.com>

tophat=/share/apps/rna_analysis/tophat/tophat-2.1.0/tophat

data="data/"

ucsc_gene="~/reference/ref_vir_det/gencode.v25.chr_patch_hapl_scaff.annotation.gtf"

index="~/reference/ref_vir_det/hg38"

p=4

#the analysis
for sample in `ls -1 $data/*.fq  | awk 'BEGIN {FS="/"} {print $NF}' | sort | grep -E -o '.*_[12]' | sed 's/_2$/_1/g' | uniq | sed 's/_1$//g'`;
    do
    echo "Aligning sample $sample"
    outdir=$sample""_aln
    echo "Outdir: $outdir"
    echo "$tophat -o $outdir -p $p -G $ucsc_gene $index $data/$sample""_1.fq $data/$sample""_2.fq" | qsub -V -cwd -l h_vmem=3G -pe smp $p -e $sample.e -o $sample.o -N tophat$sample -m ea -M atlasmaths\@yahoo.com
#Sort the bam files
    echo "samtools sort -n  $sample""_aln/unmapped.bam  -o ${sample}_sorted.bam" \
    | qsub -V -cwd -l h_vmem=2G -pe smp 2 -N sort -hold_jid tophat$sample

#Covert bam files to fastq
    echo "bedtools bamtofastq -i  ${sample}_sorted.bam -fq  ${sample}_sorted_1.fq -fq2  ${sample}_sorted_2.fq" \
    | qsub -V -cwd -l h_vmem=2G -pe smp 2 -N fastq -hold_jid sort

#alignemnet by bwa
    echo "bwa mem /home/akhan/reference/ref_vir_det/ref_vir_757/viruses_757.fasta  ${sample}_sorted_1.fq ${sample}_sorted_2.fq > aln_$sample.sam" \
    | qsub -V -cwd -l h_vmem=2G -pe smp 2 -N bwa_map -hold_jid fastq

#sam2bam
    echo "samtools view -Sb -h aln_$sample.sam > aln_$sample.bam" \
    | qsub -V -cwd -l h_vmem=2G -pe smp 2 -N sam2bam -hold_jid bwa_map

#Count the viruses
    echo "samtools view aln_$sample.bam | cut -f3 | sort | uniq -c > $sample.viruses_count.txt" \
    | qsub -V -cwd -l h_vmem=2G -pe smp 2 -N vircon -hold_jid sam2bam

#Put all viruses in one file
    echo "tail -n +1 *.txt > Virus_of_all_samples.txt" \
    | qsub -V -cwd -l h_vmem=2G -pe smp 2 -N allviruses -hold_jid vircon

    echo "samtools depth aln_$sample.bam | awk '''{if ($3>=5) print $0}''' | \
    awk '''{ if ($2!=(ploc+1)) \
    {if (ploc!=0){printf("%s %d-%d\n",$1,s,ploc);}s=$2} ploc=$2; }'''" | qsub -V -cwd -l h_vmem=2G -pe smp 2 -N continousregion -hold_jid allviruses
    echo
done

