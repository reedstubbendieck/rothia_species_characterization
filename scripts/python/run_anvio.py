#!/usr/bin/env python

import argparse, os, subprocess
from pathlib import Path
from shutil import copyfile

remove_chars = len(os.linesep)

parser = argparse.ArgumentParser(
        description='''run anvi'o pangenomics pipeline on *.fasta genome files''')

# add the parser arguments
parser.add_argument("input_dir", type=str, help="path/to/dir/with/genomes.fasta/")
parser.add_argument("output_dir", type=str, help="path/to/output/")
parser.add_argument("project", type=str, help="project name for anvi'o")
parser.add_argument("thread_num", type=str, help="thread number")

args=parser.parse_args()

input_path = args.input_dir
output_path = args.output_dir
project_name = args.project
w = args.thread_num

# make the output directories if they do not exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

if not os.path.exists(output_path+"anvio_db/"):
    os.makedirs(output_path+"anvio_db/")

if not os.path.exists(output_path+"anvio_reformatted_fasta_files/"):
    os.makedirs(output_path+"anvio_reformatted_fasta_files/")

if not os.path.exists(output_path+"anvio_pangenome/"):
    os.makedirs(output_path+"anvio_pangenome/")

# generate contigs database for anvio
## initialize external-genome dictionary

external_genome_dict = {}

for file in os.listdir(input_path):
        if file.endswith(".fasta"):
            in_prefix = file.split(".fasta")[0]
            external_genome_dict[in_prefix] = "anvio_db/"+in_prefix+".db"
            # run anvi-script-reformat-fasta to simplify contigs for anvi'object, remove contigs <1000 bp, 
            anvio_reformat_call = "anvi-script-reformat-fasta "+input_path+file+" -l 1000 --simplify-names --seq-type NT --prefix "+in_prefix+" -o "+output_path+"anvio_reformatted_fasta_files/"+in_prefix+"_clean.fasta"
            subprocess.call(anvio_reformat_call, shell=True)
            #run anvi-gen-contigs-database to generate database from fasta files
            anvio_gen_contigs_call = "anvi-gen-contigs-database -f "+output_path+"anvio_reformatted_fasta_files/"+in_prefix+"_clean.fasta"+" -o "+output_path+external_genome_dict[in_prefix]+" -n "+project_name+"_"+in_prefix+" -T "+w
            subprocess.call(anvio_gen_contigs_call, shell=True)
            # run hmms
            anvio_hmm_call = "anvi-run-hmms -c "+output_path+external_genome_dict[in_prefix]+" -T "+w
            subprocess.call(anvio_hmm_call, shell=True)

# write the external-genomes file for anvio
with open(output_path+"external_genomes", 'w', newline='') as f_output:
    # write the header line
    header = "name\tcontigs_db_path\n"
    f_output.write(header)
    for genome in external_genome_dict:
        x = genome+"\t"+external_genome_dict[genome]+"\n"
        f_output.write(x)
    # remove the last empty line from the file
    f_output.truncate(f_output.tell() - remove_chars)

# generate the genome storage file
genome_storage_call = "anvi-gen-genomes-storage -e "+output_path+"external_genomes"+" -o "+output_path+project_name+"-GENOMES.db"
subprocess.call(genome_storage_call, shell=True)

# run anvi'o
run_anvio_call = "anvi-pan-genome -g "+output_path+project_name+"-GENOMES.db"+" -n "+project_name+" --output-dir "+output_path+"anvio_pangenome/"+" --num-threads "+w+" --minbit 0.5 --mcl-inflation 10 --min-occurrence 2 --force-overwrite"
subprocess.call(run_anvio_call, shell=True)