#!/usr/bin/env python

import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description='Runs Bakta on genome sequences to predict protein coding genes')

# Add the required parser arguments
parser.add_argument("input_dir", type=str, help="Path to input directory")
parser.add_argument("output_dir", type=str, help="Path to output directory")
parser.add_argument("thread_num", type=str, help="Number of threads")

args = parser.parse_args()

input_path = args.input_dir
output_path = args.output_dir
w = args.thread_num

# Ensure output directory exists
os.makedirs(output_path, exist_ok=True)

# Get list of genome files
for file in os.listdir(input_path):
    if file.endswith(".fasta"):
        file_prefix = os.path.splitext(file)[0]
        file_path = os.path.join(input_path, file)
        output_genome_path = os.path.join(output_path, file_prefix)
        
        bakta_call = (
            f"bakta --output {output_genome_path} --prefix {file_prefix} "
            f"--strain {file_prefix} --threads {w} --force "
            f"--skip-trna --skip-tmrna --skip-rrna --skip-ncrna "
            f"--skip-ncrna-region --skip-crispr --skip-pseudo --skip-sorf "
            f"--skip-gap --skip-ori --skip-plot {file_path}"
        )
        
        print(bakta_call)
        subprocess.call(bakta_call, shell=True)