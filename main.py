import sys
import random

# ----------------- DNA --------------------


class DNA:

    # Class for DNA segments

    def __init__(self, length):
        self.helix = []
        self.length = length
        self.strand_0 = self.gen_strand(length)
        self.strand_1 = self.gen_strand(length)
        self.fix_strand()  # turns pairs to match rule A - T and C - G
        self.build_helix()  # combine strands into the DNA structure.

    @staticmethod
    def gen_strand(length):
        # Randomly generate a strand of DNA
        compounds = ['a', 't', 'c', 'g']
        strand = []

        for i in range(length):

            c = random.choice(compounds)

            strand.append(c)

        return strand

    def fix_strand(self): # Manipulating to agree with (A-T, C-G)
        for i in range(self.length):
            if self.strand_0[i] == 'a' and self.strand_1[i] != 't':
                self.strand_1[i] = 't'
            if self.strand_0[i] == 't' and self.strand_1[i] != 'a':
                self.strand_1[i] = 'a'
            if self.strand_0[i] == 'c' and self.strand_1[i] != 'g':
                self.strand_1[i] = 'g'
            if self.strand_0[i] == 'g' and self.strand_1[i] != 'c':
                self.strand_1[i] = 'c'

    def print_pairs(self):
        # Prints the dna strand in pairs of three
        for i in range(self.length):
            print(self.helix[i])

    def strand_to_proteins(self):
        # Converts the codon strand to corresponding proteins
        pass

    @staticmethod
    def make_pair(a, b):
        pair = [a, b]
        return pair

    def build_helix(self):
        for i in range(self.length):
            self.helix.append(self.make_pair(self.strand_0[i], self.strand_1[i]))


# ---------------- MAIN --------------------

def main():

    # Some starter stuff

    base_pairs = 2000  # size of dna strand
    m = 200  # multiply dna size by m
    p = 20  # forward and backward primers
    d = 200
    e = 50

    r = random.randint(-e, e)

    processivity = d + r

    print("Processivity: ", processivity)

    dna = DNA(base_pairs)

    dna.print_pairs()


main()  # Run the program

