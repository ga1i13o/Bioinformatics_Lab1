from .read_objects import FastaObj
import numpy as np
from statistics import mode


class ConsensusFinder(object):
    def __init__(self, in_file=""):
        self.input_file = in_file
        self.fragments = []
        self.consensus = []

    def find_consensus(self):
        self.__load_fragments()
        self.__group_fragments()
        print("[!!] All done [!!]")

    def write_output(self, output_file="out_consensus.txt"):
        print(f"[!!] Output dumped to {output_file} [!!]")
        with open(output_file, "w") as out_file:
            for read in self.consensus:
                out = read + '\n'
                out_file.write(out)

    def __group_fragments(self):
        print("[!!] Constructing consensus... [!!]")
        begin_region = 0
        end_region = 1
        for i in range(1, len(self.fragments)):
            if self.fragments[i][1] >= self.fragments[i-1][1] + self.fragments[i-1][0].length:
                end_region = i
                self.consensus.append(self.__extract_consensus(begin_region, end_region))
                begin_region = i
        if end_region != len(self.fragments) - 1:
            end_region = len(self.fragments)
            self.consensus.append(self.__extract_consensus(3, end_region))

    def __extract_consensus(self, begin, end):
        n_fragments = end-begin
        consensus_start_position = self.fragments[begin][1]
        consensus_length = self.fragments[end-1][1] +\
                           self.fragments[end-1][0].length -\
                           self.fragments[begin][1]
        consensus_result = ""
        consensus_matrix = np.zeros(shape=(n_fragments,
                                            consensus_length), dtype=int)

        for i in range(n_fragments):
            consensus_matrix[i][self.fragments[begin+i][1] - consensus_start_position:\
                                self.fragments[begin+i][1]+self.fragments[begin+i][0].length - consensus_start_position] =\
                        [ord(base) for base in self.fragments[begin+i][0].read]
        for i in range(consensus_length):
            if consensus_matrix[:,i].sum() % consensus_matrix[:,i].max() != 0:
                consensus_result += chr(mode(consensus_matrix[:,i]))
            else:
                consensus_result += chr(consensus_matrix[:,i].max())
        return consensus_result

    def __load_fragments(self):
        print("[!!] Loading fragments... [!!]")
        with open(self.input_file, "r") as in_file:
            lines = in_file.readlines()
        for line in lines:
            fields = line.split(" ")
            fasta_read = FastaObj(id_line=fields[0], read=fields[1])
            self.fragments.append((fasta_read, int(fields[2].strip())))
        self.fragments.sort(key=lambda x: x[1])

    @property
    def input_file(self):
        return self.__input_file

    @input_file.setter
    def input_file(self, value):
        self.__input_file = value
        if "." in value:
            self.filetype = value.split(".")[1]