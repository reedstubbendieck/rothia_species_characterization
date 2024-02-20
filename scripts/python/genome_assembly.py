#!/usr/bin/python

# uses fastp to quality trim reads and spades for genome assembly

import argparse, glob, os, subprocess

# parse command line arguments

parser = argparse.ArgumentParser(
        description='''uses fastp and spades to assemble genomes from paired-end Illumina sequecing reads.''')

# add the parser arguments
parser.add_argument("input_dir", type=str, help="path/to/dir/with/inputs/")
parser.add_argument("output_dir", type=str, help="path/to/output/dir/")
parser.add_argument("threads_num", type=str, help="number of threads")

args=parser.parse_args()

input_path = args.input_dir
output_path = args.output_dir
threads = args.threads_num

# generate output directories if needed
if not os.path.exists(output_path):
    os.makedirs(output_path)

if not os.path.exists(output_path+"/trimmed_reads/"):
    os.makedirs(output_path+"/trimmed_reads/")

if not os.path.exists(output_path+"/genome_assemblies/"):
    os.makedirs(output_path+"/genome_assemblies/")

if not os.path.exists(output_path+"/plasmid_assemblies/"):
    os.makedirs(output_path+"/plasmid_assemblies/")

if not os.path.exists(output_path+"/final/"):
    os.makedirs(output_path+"/final/")

# retrieve the sequence paths for the reads

for root, dirs, files in os.walk(input_path):
    for dir in dirs:
        prefix = dir
        reads = []
        for file in os.listdir(input_path+prefix+"/"):
            if file.endswith(".fastq.gz"):
                reads.append(input_path+prefix+"/"+file)
        if not os.path.exists(output_path+"/trimmed_reads/"+prefix):
            os.makedirs(output_path+"/trimmed_reads/"+prefix)
        fastp_call = "fastp -i "+reads[0]+" -I "+reads[1]+" -o "+output_path+"trimmed_reads/"+prefix+"/"+os.path.basename(reads[0])+" -O "+output_path+"trimmed_reads/"+prefix+"/"+os.path.basename(reads[1])
        subprocess.call(fastp_call, shell=True)
        spades_call = "spades.py --isolate -t "+threads+" --pe1-1 "+output_path+"trimmed_reads/"+prefix+"/"+os.path.basename(reads[0])+" --pe1-2 "+output_path+"trimmed_reads/"+prefix+"/"+os.path.basename(reads[1])+" -o "+output_path+"genome_assemblies/"+prefix
        subprocess.call(spades_call, shell=True)
        plasmid_call = "spades.py --plasmid -t "+threads+" --pe1-1 "+output_path+"trimmed_reads/"+prefix+"/"+os.path.basename(reads[0])+" --pe1-2 "+output_path+"trimmed_reads/"+prefix+"/"+os.path.basename(reads[1])+" -o "+output_path+"/plasmid_assemblies/"+prefix
        subprocess.call(plasmid_call, shell=True)
        rename_call = "cp "+output_path+"/genome_assemblies/"+prefix+"/contigs.fasta "+output_path+"/final/"+prefix+".fna"
        subprocess.call(rename_call, shell=True)
        plasmid_rename_call = "cp "+output_path+"/plasmid_assemblies/"+prefix+"/contigs.fasta "+output_path+"/final/"+prefix+"_plasmids.fna"
        subprocess.call(plasmid_rename_call, shell=True)
