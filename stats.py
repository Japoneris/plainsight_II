"""
Script to evaluate corpus / tree / message size ...
"""

import argparse
import os

from src import plain

def sort_dict(dic, reverse=True):
    """For a dict {key: int/float}, 
    sort keys by decreasing values
    :param dic: {key: int/float}
    :rparam: {k1: v1, k2:v2, ...} | v1 > v2
    :type param: dict
    :rtype: dict
    """
    return dict(sorted(dic.items(), key=lambda x: (-x[1], x[0]), reverse=reverse)[::-1])

def get_avg_node(tree):
    """Count the number of children per node

    Gives an idea of the encoding power 
    """
    dic = {len(tree.children): 1}
    for c in tree.children:
        dic_i = get_avg_node(c)
        for i, vi in dic_i.items():
            if i not in dic:
                dic[i] = vi
            else:
                dic[i] += vi
    
    return sort_dict(dic)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    #parser.add_argument("action", choices=["encode", "decode"],
    #        help="Action to perform: encode or decode.")


    parser.add_argument("corpus", type=str,
            help="Location of the corpus file.")
    parser.add_argument("--depth", type=int, default=2,
            help="Depth of the tree. At least 1.")

    
    parser.add_argument("--message", type=str,
            default="",
            help="""Message to encode.
            - If a file exists, then open and read the file.
            - If no path exists, consider this input as the message to encode.""")
    
    parser.add_argument("--method", choices=["Binary", "Huffman"], default="Huffman",
            help="Depth of the tree. At least 1.")

    parser.add_argument("--save_path", default="examples/test.txt",
            help="Where to save the result.")

    parser.add_argument("-v", "--verbose", default=False, action="store_true",
            help="Make the script speak")

    args = parser.parse_args()

    d = args.depth
    assert(d > 0)
    assert(isinstance(d, int))
    assert(os.path.exists(args.corpus))






    print("="*40)
    print("Loading the corpus")
    corpus = []
    with open(args.corpus, "r") as fp:
        corpus = fp.readlines()

    print("Gathered {} sentences".format(len(corpus)))


    # Preprocessing the corpus
    # Suppose we only need to split space / everything is lower case

    # Initialization
    print("="*40)
    print("Tree initialization. \n\tMethod: {}\n\tDepth: {}".format(args.method, args.depth))
    tree = plain.Tree(depth=d)

    # Build n-grams
    for sentence in corpus:
        seq = ["<TOP>"] + sentence.split() + ["<BOT>"]
        for i in range(len(seq)-1): # -1 because do not iterate over BOT
            tree.update(seq[i:i+d])

    if args.method == "Huffman":
        for c in tree.children:
            c.clean_huffman()
    else:
        for c in tree.children:
            c.clean_pow2()

    print("="*40)

    print("0: leaf terminal nodes")
    print("1: trivial node that cannot encode.")
    print("last: total number of n-grams")
    print("-"*40)

    dico = get_avg_node(tree)
    for i, vi in dico.items():
        print("{}\t{}".format(i, vi))

    
    print("Encoding power:")
    cnt_1 = dico[1] # Number of non-encoding nodes
    cnt_0 = dico[0] # Number of leaves, i.e. number of n-grams
    cnt = sum(dico.values()) # Total number of nodes
    print("\t{:.4} %".format(100. * (1 - cnt_1 / (cnt-cnt_0))))

    #### Optional 
    if args.message != "":
        print("="*40)
        print("Loading the message")
        message = ''
        if os.path.exists(args.message):
            print("Found a file")
            with open(args.message, "r") as fp:
                message = fp.read()

        else:
            print("No file found: Using `{}` as the message to hide".format(args.message))
            message = args.message


        encoded_message = plain.encode(tree, message)
        n0 = len(message)
        n1 = len(encoded_message.split())

        print("Message size:")
        print("\t{} \t characters".format(n0))
        print("\t{} \t bits".format(8 * n0))

        print()
        print("Encoded message size:")
        print("\t{} \t characters".format(len(encoded_message)))
        print("\t{} \t words".format(n1))
        
        print("Inverse Ratio (words/bit): ")
        print("\t{:.4}".format(float(n1/(8*n0))))




