from argparse import ArgumentParser, ArgumentTypeError, HelpFormatter
from convertFQ.version import __version__
import sys

def get_args():
    parser = ArgumentParser(description="convertFQ: RNA -> DNA | DNA -> RNA")
    parser.add_argument("-v", "--version",help="Print version and exit.",action="version",version='ConvertFQ {}'.format(__version__))
    parser.add_argument("-i", "--input", required=True, help="Input FASTQ [Required]")
    parser.add_argument("-c", "--conversion", required=True, type=str, help="rna2dna | dna2rna [Required]")
    parser.add_argument("-o", "--output", required=True, type=str, help="output name [Required]")
    args = parser.parse_args()
    return args