from genominator import seq_gen
import argparse
import sys


def parse_arguments():
    parser = argparse.ArgumentParser(description="generates fake fasta or fastq files")
    parser.add_argument("filetype", help="specify name and extension of output file",
                        type=str)
    parser.add_argument("n_reads", help="number of reads to generate",
                        type=int)
    parser.add_argument('probabilities', nargs='+', help='Probability of having A,T,C,G',
                        type=float)

    args = parser.parse_args()
    filename = args.filetype
    if filename.split(".")[1] not in ["fa", "fq"]:
        print("filetype has to be either \".fa\" or \".fq\"")
        sys.exit(-1)
    probs = args.probabilities
    if len(probs) != 4:
        print("you have to enter all 4 probabilities")
        sys.exit(-1)
    if sum(probs) not in [1, 10, 100]:
        print("probabilities should sum to 1")
        sys.exit(-1)
    probs = list(map(lambda x: x/sum(probs), probs))
    settings = {"probs": probs, "filename": filename, "reads": args.n_reads}

    return settings


def main(settings):
    generator = seq_gen.SequenceGenerator(filename=settings["filename"],
                                          n_reads=settings["reads"],
                                          probs=settings["probs"])
    print(f"Probabilities:\n\t{generator.probs_list}")
    generator.generate_file()
    print("The file has been generated. Exiting...")


if __name__ == '__main__':
    settings = parse_arguments()
    print(f"[||||] Output file will be '{settings['filename']}' and will contain {settings['reads']} reads [|||]")
    main(settings)

