import sys
import random

# ----------------- DNA --------------------

class DNA:

    # Class for DNA segments

    def __init__(self, len):
        self.len = len
        self.strand_0 = self.gen_strand(len)
        self.strand_1 = self.gen_strand(len)
        self.struct = self.build_struct()

    @staticmethod
    def gen_strand(len):
        # Randomly generate a strand of DNA\
        compounds = ['a', 't', 'c', 'g']
        strand = []
        # codon = []

        # make pairs of three
        counter = 0

        # Figure this issue out, needs 3 per pair, not 2

        for i in range(len):

            c = random.choice(compounds)
            # codon.append(c)
            # counter += 1

            strand.append(c)

            # if counter == 3 and i < len:
                # counter = 0
                # strand.append(codon)
                # codon.clear()

        return strand

    def print_pairs(self):
        # Prints the dna strand in pairs of three
        for i in range(self.len):
            print(self.strand_0[i], " - ", self.strand_1[i])

        # print(self.strand_0)
        # print(self.strand_1)

    def strand_to_proteins(self):
        # Converts the codon strand to corresponding proteins

        pass

    @staticmethod
    def make_pair(a, b):
        pair = [a, b]
        return pair

    def build_struct(self):
        struct = []

        s_0 = self.strand_0
        s_1 = self.strand_1

        for i in range(self.len):
            struct.append(self.make_pair(s_0[i], s_1[i]))

        return struct


# ---------------- MAIN --------------------

def main():

    # Some starter stuff

    base_pairs = 2000
    m = 200
    p = 20
    d = 200
    e = 50

    r = random.randint(-e, e)

    processivity = d + r

    print("Processivity: ", processivity)

    dna = DNA(base_pairs)

    # dna.print_pairs()

    print(dna.struct)

# Run the program
main()

