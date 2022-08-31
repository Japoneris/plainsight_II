import math
import random

class Tree:

    def __init__(self, depth=2, name="ROOT"):
        self.depth = depth
        self.name  = name 
        self.freq  = 0
        self.code  = ""
        self.children = []
        self.child_name = [] # shortcut to find position

    def update(self, seq):
        """Update the node with one new sequence
        """
        self.freq += 1

        if seq == []:
            return 
        
        else:
            na = seq.pop(0) # Warning: list size modification
            if na in self.child_name:
                i = self.child_name.index(na)
                self.children[i].update(seq)

            else:
                self.child_name.append(na)
                node = Tree(self.depth, name=na)
                node.update(seq)
                self.children.append(node)

    def set_bin_code(self, i, k):
        """
        :param i: value of the code
        :param k: power of 2
        """
        self.code =  bin(i)[2:].zfill(k)
        return
    
    def set_string_code(self, code):
        """When the code is already a string
        """
        self.code = code
        return

    def clean_pow2(self):
        """
        1. Keep valid nodes
        2. For valid nodes, assign a code
        """

        k  = len(self.children)
        if k <= 1:
            return
        
        nk = int(math.log2(k))
        k  = int(2**nk) # keep the lowest power of 2
        
        # Sort lexicographic and frequency.
        # Keep the k best items
        # The minus is to get decreasing frequency AND ascending lexicographic
        self.children   = sorted(self.children, key=lambda x: (-x.freq, x.name))[:k]
        self.child_name = list(map(lambda x: x.name, self.children))
        
        
        # Add a binary code to each item
        list(map(lambda x: x[1].set_bin_code(x[0], nk), enumerate(self.children)))
        
        # Iterate over childrens
        list(map(lambda x: x.clean_pow2(), self.children))

        return

    def _get_huffman(self, freqs):
        """
        Find huffman code using the frequencies

        :param freqs: list of frequencies
        :rparam: Codes associated to the frequencies
        """
        # List with (freq, [ID])
        lst = sorted(map(lambda x: (x[1], [x[0]]), enumerate(freqs)))
        
        # Initialize code words
        dic_code = dict([(ID, '') for ID, _ in enumerate(lst)])

        while len(lst) > 1:
            # The first one has the lowest frequency, which would get a 1
            m1, m0 = lst[0], lst[1]
            
            # Iterate over all the IDs, and happend a 1 or a 0
            for c in m1[1]:
                dic_code[c] = "1" + dic_code[c]
            for c in m0[1]:
                dic_code[c] = "0" + dic_code[c]

            f_tot  = m1[0] + m0[0]
            ID_tot = m1[1] + m0[1] # List concatenation

            # For very large list of words, this is not optimal
            # It does the job for small input.
            lst = sorted([(f_tot, ID_tot)] + lst[2:])
        
        return list(dic_code.values())



    def clean_huffman(self):
        """
        Huffman coding.
        Keep all words, add them a code word based on their frequency
        """

        # Compute codes
        codes = self._get_huffman(list(map(lambda x: x.freq, self.children)))
        
        # Update codes
        for idx, c in enumerate(codes):
            self.children[idx].set_string_code(c)
        
        return


    def get_word(self, seq, bits):
        """For encoding, find the right code.

        If sequence is too long compare to tree depth: return ("", "")

        :param seq: list of words
        :param bits: bitstring to encode
        :rparam: (encoding word, bits left)
        """
        if seq == []:
            # End of the context. 
            # Check bits
            if len(self.children) == 1:
                # Single choice. Stop here
                return (self.child_name[0], bits)
            
            
            bits_pad = bits + "0" * 8 # 8 is sufficient

            cands = list(filter(lambda x: bits_pad.startswith(x.code), self.children))
            # Normally, one candidate.
            if len(cands) == 1:
                c = cands[0]
                return (c.name, bits[len(c.code):])

            elif len(cands) == 0:
                print("No code found...")
                assert(False)
            else:
                #print("Too many solutions ...")
                # Happens when start the tree
                i = random.randint(0, len(cands)-1)
                return (cands[i].name, bits)

        
        else:
            # Move in the tree
            i = self.child_name.index(seq[0])
            return self.children[i].get_word(seq[1:], bits)


    
    def get_code(self, seq):
        """
        For decoding, find the associated code.
        
        :param seq: list of words
        :rparam: string of 0/1
        """
        if seq == []:
            return self.code
        else:
            i = self.child_name.index(seq[0])
            return self.children[i].get_code(seq[1:])

        
### Encode / Decode function
        
def encode(tree, message):
    """
    Encode a message into a spam
    
    :param tree: Tree storing words transition
    :param message: ASCII message to encode
    :rparam: encoded message
    :rtype: str
    :type message: str
    """
    d = tree.depth
    d1 = d-1

    # Convert the message to a string of 0/1
    message_bin = "".join(list(map(lambda x: bin(ord(x))[2:].zfill(8), message)))
    context = ["<TOP>"]

    message_mem  = [] # list of sentences
    message_code = [] # current sentence

    while len(message_bin) > 0:
        wd, message_bin = tree.get_word(context, message_bin)

        if wd == '<BOT>':
            # Reset
            context = ['<TOP>']
            message_mem.append(" ".join(message_code))
            message_code = []

        else:
            # Extend the current sentence
            message_code.append(wd)
            context.append(wd)


            if len(context) > d1:
                context = context[-d1:]
                # Remove when too many 
    # End of the loop
    if len(message_code) > 0:
        # Add the current sentence to the full message.
        message_mem.append(" ".join(message_code))

    return "\n".join(message_mem)


def decode(tree, message):
    """Decode an encoded message
    
    :param tree: Tree storing words transition
    :param message: ASCII message to decode. Words must belong to the tree vocabulary
    :rparam: decoded message
    :rtype: str
    :type message: str
    """
    d = tree.depth
    
    message_mem = message.split("\n")
    context = []
    message_code = []
    bin_list = []

    while (message_mem != []) | (message_code != []):

        if message_code == []:
            # Take a new sentence if no words left
            message_code = message_mem.pop(0).split()
            context = ["<TOP>"]

        # Remove one item from the input, add it to the context
        context.append(message_code.pop(0))
        if len(context) > d:
            context = context[-d:]

        # Find the corresponding code
        b = tree.get_code(context)
        bin_list.append(b)

    bin_string = "".join(bin_list)
    n_bytes = len(bin_string) // 8
    char_list  = [chr(int(bin_string[8*i:8*(i+1)], 2)) for i in range(n_bytes)]
    
    return "".join(char_list)


