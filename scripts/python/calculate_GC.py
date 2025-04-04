#!/usr/bin/env python

import argparse, os

parser = argparse.ArgumentParser(
        description='''Calculate GC% of all .fna sequences in a specified directory''')

# add the parser arguments
parser.add_argument("input_dir", type=str, help="path/to/dir/with/fna/sequences/")

args=parser.parse_args()

input_path = args.input_dir

def calculate_gc_percentage(sequence):
    total_bases = len(sequence)
    gc_count = sequence.count('G') + sequence.count('C')
    gc_percentage = (gc_count / total_bases) * 100
    return round(gc_percentage, 2)

def process_fasta_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    sequences = []
    current_sequence = ''
    for line in lines:
        if line.startswith('>'):
            if current_sequence:
                sequences.append(current_sequence.upper())
                current_sequence = ''
        else:
            current_sequence += line.strip()

    if current_sequence:
        sequences.append(current_sequence.upper())

    gc_percentage = 0.0
    total_bases = 0
    for sequence in sequences:
        gc_count = sequence.count('G') + sequence.count('C')
        sequence_bases = len(sequence)
        gc_percentage += (gc_count / sequence_bases) * sequence_bases
        total_bases += sequence_bases

    if total_bases > 0:
        gc_percentage = (gc_percentage / total_bases) * 100
        gc_percentage = round(gc_percentage, 2)

    return gc_percentage


def calculate_gc_percentages_in_directory(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if file_path.endswith(".fasta"):
            if os.path.isfile(file_path):
                gc_percentage = process_fasta_file(file_path)
                file_name_without_extension = os.path.splitext(file_name)[0]
                print(f"{file_name_without_extension},{gc_percentage}")



calculate_gc_percentages_in_directory(input_path)
