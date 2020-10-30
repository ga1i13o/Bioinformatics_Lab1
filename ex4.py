from genominator import aligners
import argparse
import sys
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description="compares to fasta files to find common reads")
    parser.add_argument("align", help="file containing the alignment",
                        type=str)

    args = parser.parse_args()
    input_file = args.align

    if not os.path.isfile(input_file):
        print(f"{input_file} does not exist")
        sys.exit(-1)
    settings = {"input": input_file}

    return settings


def main(settings):
    consensus = aligners.ConsensusFinder(settings['input'])
    consensus.find_consensus()
    consensus.write_output()


if __name__ == '__main__':
    settings = parse_arguments()
    main(settings)

