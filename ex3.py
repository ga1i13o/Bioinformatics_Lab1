from genominator import compare
import argparse
import sys
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description="compares to fasta files to find common reads")
    parser.add_argument("file_1", help="firt input file to be analyzed",
                        type=str)
    parser.add_argument("file_2", help="second input file to be analyzed",
                        type=str)
    parser.add_argument("outp", help="output file",
                        type=str)

    args = parser.parse_args()
    inputs = [args.file_1, args.file_2]

    for input_file in inputs:
        if input_file.split(".")[1] not in ["fa", "fq"]:
            print("both input filetype has to be either \".fa\" or \".fq\"")
            sys.exit(-1)
        if not os.path.isfile(input_file):
            print(f"{input_file} does not exist")
            sys.exit(-1)
    settings = {"input_1": inputs[0], "input_2": inputs[1], "output": args.outp}

    return settings


def main(settings):
    comparator = compare.Comparator(settings['input_1'], settings['input_2'],
                                    settings['output'])
    comparator.load_file()
    comparator.compare_files()
    comparator.write_output()


if __name__ == '__main__':
    settings = parse_arguments()
    print(f"[||||] Output file will be '{settings['output']}' [|||]")
    main(settings)

