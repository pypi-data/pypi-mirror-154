from Bio import SeqIO
from Bio import Seq
import convertFQ.utils as utils
import sys


def main():
    args = utils.get_args()
    if str(args.conversion) == 'rna2dna':
        rna2dna(args.input, args.output)
        
    elif str(args.conversion) == 'dna2rna':
        dna2rna(args.input, args.output)
        
    else:
        print('Sorry '+str(args.conversion)+' is wrong option\nPlease use eihter "rna2dna" or "dna2rna"')

def rna2dna(FASTQIN, FASTQOUT):
    print('Converting RNA to DNA ...\n')
    new_records = []
    for record in SeqIO.parse(FASTQIN, "fastq"):
        sequence = str(record.seq)
        letter_annotations = record.letter_annotations

        # You first need to empty the existing letter annotations
        record.letter_annotations = {}

        new_sequence = sequence.replace('U','T')
        record.seq = Seq.Seq(new_sequence)


        new_letter_annotations = {'phred_quality': letter_annotations['phred_quality']}
        record.letter_annotations = new_letter_annotations

        new_records.append(record)

    with open(str(FASTQOUT)+'.fastq', 'w') as output_handle:
        SeqIO.write(new_records, output_handle, "fastq")

def dna2rna(FASTQIN, FASTQOUT):
    print('Converting DNA to RNA ...\n')
    new_records = []
    for record in SeqIO.parse(str(FASTQIN), "fastq"):
        sequence = str(record.seq)
        letter_annotations = record.letter_annotations

        # You first need to empty the existing letter annotations
        record.letter_annotations = {}

        new_sequence = sequence.replace('T','U')
        record.seq = Seq.Seq(new_sequence)


        new_letter_annotations = {'phred_quality': letter_annotations['phred_quality']}
        record.letter_annotations = new_letter_annotations

        new_records.append(record)

    with open(str(FASTQOUT)+'.fastq', 'w') as output_handle:
        SeqIO.write(new_records, output_handle, "fastq")

if __name__ == '__main__':
    main()
