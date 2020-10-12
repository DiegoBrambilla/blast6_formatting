#!/usr/bin/python

import io
import sys
import pandas as pd
import click

"""
Example usage:
    python BLAST6_filter.py --input-file example_annotation_table.m8 --min-length 37 --perc-identity 90 > my-output.tsv
"""
#Create function that reads BLAST6 tables and edit them as follows
#You need to provide minimum alignment length and identity percentage
#as they are argument of the function
def read_filter_sort(file_name, min_length, perc_identity):
#Import the table and provide specific column name
    data = pd.read_csv(file_name, sep="\t", index_col=False, header=None, names=["identifier", "descriptor","pident", "alignment_length", "mismatch", "gapopen", "qstart", "qend", "sstart", "send", "evalue", "bitscore"])
#Filter rows based on the alignment length value
    data_minlen = data.loc[data["alignment_length"] >=float(min_length)]
#Filter rows based on the identity percentage
    data_filtered = data_minlen.loc[data_minlen["pident"] >=float(perc_identity)]
#Sort unique rows based on the read identifier    
    data_sorted = data_filtered.sort_values(by=["identifier"])
    return data_sorted

def write_data(data):
#Write to output, the command below does not work
#provide a header to the output file
#    print('identifier'\t'descriptor'\t'pident'\t'alignment_length'\t'mismatch'\t'gapopen'\t'qstart'\t'qend'\t'sstart'\t'send'\t'evalue'\t'bitscore')
    for index, row in data.iterrows():
        identifier = row ["identifier"]
#Replace pipe symbol with tabs, thus creating new columns
        descriptor = row ["descriptor"]#.replace("|", "\t")
        pident = row ["pident"]
        alignment_length = row ["alignment_length"]
        mismatch = row ["mismatch"]
        gapopen = row ["gapopen"]
        qstart = row ["qstart"]
        qend = row ["qend"]
        sstart = row ["sstart"]
        send = row ["send"]
        evalue = row ["evalue"]
        bitscore = row ["bitscore"]
#The format function has been applied to the fstrings like this: {:.f}
#But {:.f} does not help writing the correct number of decimals to file
        print(f"{identifier}\t{descriptor}\t{pident:.3f}\t{alignment_length}\t{mismatch}\t{gapopen}\t{qstart}\t{qend}\t{sstart}\t{send}\t{evalue:5f}\t{bitscore}")

@click.command()
@click.option("--input-file", help="The input .m8 file to process. must be in BLOSUM62 format, without straying from the default.")
@click.option("--min-length", type=int, help="Minimum alignment length.")
@click.option("--perc-identity", type=int, help="Minimum identity percentage.")
def main(input_file, min_length, perc_identity):
    data = read_filter_sort(input_file, min_length, perc_identity)
    write_data(data)

if __name__ == "__main__":
    main()

