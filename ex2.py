from genominator import statista
import argparse
import sys
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description="extracts statistics from fasta/fastq files")
    parser.add_argument("input", help="input file to be analyzed",
                        type=str)
    parser.add_argument("output", help="output file to dump statistics to",
                        type=str)
    parser.add_argument("-gc", "--threshold", help="GC_THRESHOLD for GC content",
                        type=int)

    args = parser.parse_args()
    input_file = args.input
    if input_file.split(".")[1] not in ["fa", "fq"]:
        print("input filetype has to be either \".fa\" or \".fq\"")
        sys.exit(-1)
    if not os.path.isfile(input_file):
        print("Input file does not exist")
        sys.exit(-1)
    settings = {"input": input_file, "output": args.output, "thresh":args.threshold}

    return settings


def main(settings):
    stats = statista.Statista(settings['input'], settings['thresh'])
    stats.set_operations(["basis_number", "low_complex_seqs", "gc_content"])
    print(stats.ops_to_perform)
    stats.compute_stats()
    stats.write_output(settings['output'])


if __name__ == '__main__':
    settings = parse_arguments()
    print(f"[||||] Output file will be '{settings['output']}' and will contain stats from {settings['input']} [|||]")
    main(settings)

