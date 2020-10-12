# blast6_formatting
How to manipulate BLAST6 format tables through code.

Table of contents

  * [Goals](#goals)
  * [Steps](#steps)
  * [Background](#background)
  * [Script & challenges](#script---challenges)
  * [Test](#test)

## Goals

- For each read identifier, obtain the best hit.
- Filter best hits according to an alignment length and identity thresholds

Usually hits are listed starting from the best hit, so one way would be to sort the entries on the first column "read_identifier" so that you have unique identifiers (See Background, below). Alterantively, select, for each read identifier, the row containig the lowest "eval" value and the highest "bitscore" value.

## Steps

At the end of the annotation process (See Background, below) you obtain a table with several hits for each reads, plus the some metrics.
You want to keep only the **best hits**. That is, those with the best quality and statistics metrics. 

The steps to reach said goal are:

- sort unique hits for each read, by keeping only the first result (hit row) according to the first column of the table, whose header is the read identifier (read_ID).
- separate the text in the cells containing the database description, by substituting the pipe (|) symbols with tabs. This will create additional columns in the tabular file.
- keep only rows that have "alignmentlength" and "pident" values equal or greater than a certain value (e.g.: alignmentlength >= 37 && pident >= 90)

The anotation tables can be edited the way you would edit tabular files, but they are **headerless** by default.

## Background

Table editing is fundamental in data science.
One of bioinformatic's applications concerns the analysis of fragments of genetic material from samples (e.g.: animal tissues, water, soil, etc.).
Samples get processed in the lab and eventually the fragments of genetic material are collected into very big text files (approx. some GB). Each fragment is called "read" after it is "converted into a text file, and it is represented by a string of letters (mainly: A,T,G,C).
An identifier, which is a unique label, is associated to each read (along with other info which are not relevant for this example...).

The core of the reads analysis is the so-called annotation step.
During annotation you associate reads that pass certain cutoffs (see below for annotation quality & statistics metrics) with entries in a database.
Each database entry associate text strings (same as the ones used for the reads) to a description of the corresponding properties of the text string (e.g.: the database entry is a gene with a specific function).
Annotation help you give a meaning to reads, that is what is contained in the reads.

The annotation program (for those curious, the most popular one is BLAST) is heuristic, meaning that it employs a "shortcut" to get to the result that does not necessarily yield the theoretically best result.
Thus, the annotation program porposes several results (a.k.a. hits) for each read.
The default output format is called BLAST6 (.m8 file extension), see [here](http://www.metagenomics.wiki/tools/blast/blastn-output-format-6) for more information
The most important quality and statistics metrics of hits are:

- _pident_: read-database entry degree of identity (in percentage)
- _alignmentlength_:nuber of characters that have aligned(alignment length)
- _mismatch_: number of mismatches between the read and the database entry allowed
- _gapopen_: number of gaps (read characters that didn't find a match)
- _evalue_: the probability that matches BLAST would find by random chance, when applied to a similar database with no "true" matches.
- _bitscore_: similar interpretation as for e-value, but the higher it is the most significant the match.
You will find all said features of the annotation output summarized in this example:
```
$ head -n 2 example.m8

read_ID [...]  pident  alignmentlength  mismatch  gapopen [...] evalue  bitscore 
ERR1995198.10006378.1 [...] 91.8  49  4 0 [...] 3.8e-23 98.2
```
## Script & challenges

What the script does:

- Read file, filter rows according to threshold and writes to output file
- Allows to set I/O file names and thresholds on command line

What needs to be done:

- The script writes value as floats, thus reporting incorrect decimals.
read numbers as both string and as float, do the filtering based on the floats and then print out only the string
- The script does not print the headers to the output file (optional feature)

## Test

A test case can be run by using the test files provided under test/ :
```
$ python BLAST6_filter.py --input-file example_annotation_table.m8 --min-length 37 --perc-identity 90 > my-output.tsv
```
Dependencies: python >=3.6, pandas, click
