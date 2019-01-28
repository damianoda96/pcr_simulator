import sys
import random

# ----------------- DNA --------------------

class DNA:
    # Class for DNA segments
    def __init__(self, len):
        self.len = len
        self.strand = self.gen_strand(len)

    @staticmethod
    def gen_strand(len):
        # Randomly generate a strand of DNA\
        compounds = ['a', 't', 'c', 'g']
        strand = ""

        for i in range(len):

            c = random.choice(compounds)
            strand += c

        return strand

    def print_pairs(self):
        # Prints the dna strand in pairs of three

        pass

    def strand_to_proteins(self):
        # Converts the codon strand to corresponding proteins

        pass

# ---------------- MAIN --------------------

def main():
    #print("Hello")

    base_pairs = 2000
    m = 200
    p = 20
    d = 200
    e = 50

    r = random.randint(-e, e)

    processivity = d + r

    dna = DNA(base_pairs)

    print(dna.strand)

# Run the program
main()

