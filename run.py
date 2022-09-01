#!/usr/bin/python3

import argparse
import os

from src import plain 

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["encode", "decode"], 
            help="Action to perform: encode or decode.")

    parser.add_argument("message", type=str, 
            help="""Message to encode.
            - If a file exists, then open and read the file.
            - If no path exists, consider this input as the message to encode.""")

    parser.add_argument("corpus", type=str, 
            help="Location of the corpus file.")
    parser.add_argument("--depth", type=int, default=2, 
            help="Depth of the tree. At least 1.")

    parser.add_argument("--method", choices=["Binary", "Huffman"], 
            default="Huffman", 
            help="""Encoding method:
            - Binary is highly likely to fail
            - Huffman always succeed.""")

    parser.add_argument("--save_path", 
            default="examples/test.txt", 
            help="Where to save the result.")
    
    parser.add_argument("-v", "--verbose", action="store_true",
            default=False,
            help="Print encoded/decoded message.")
    
    """
    parser.add_argument("-c", "--character", action="store_true",
            default=False,
            help="Corpus read at the character level (select a large d).")
    """

    args = parser.parse_args()

    d = args.depth
    assert(d > 1)
    assert(isinstance(d, int))
    assert(os.path.exists(args.corpus))


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

    print("{} characters".format(len(message)))


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
    # Word transition
    for sentence in corpus:
        seq = ["<TOP>"] + sentence.split() + ["<BOT>"]
        for i in range(len(seq)-1): # -1 because do not iterate over BOT token
            tree.update(seq[i:i+d])


    if args.method == "Huffman":
        for c in tree.children:
            c.clean_huffman()
    else: # Binary
        for c in tree.children:
            c.clean_pow2()

    print("="*40)

    # Message processing
    if args.action == "encode":
        print("Encoding")
        
        encoded_message = plain.encode(tree, message)
            


        print("==> Converted into {} words".format(len(encoded_message.split())))
        
        print("Saving the message at {}".format(args.save_path + ".enc"))
        with open(args.save_path + ".enc", "w") as fp:
            fp.write(encoded_message)
        
        
        if args.verbose:
            print()
            print("=== Message: ===")
            print(encoded_message)


    elif args.action == "decode":
        print("Decoding")

        decoded_message = plain.decode(tree, message)
    
        print("==> Revovered {} characters".format(len(decoded_message)))

        print("Saving the message at {}".format(args.save_path + ".dec"))
        with open(args.save_path + ".dec", "w") as fp:
            fp.write(decoded_message)


        if args.verbose:
            print()
            print("=== Message: ===")
            print(decoded_message)


    else:
        # Not possible to get there
        assert(False)


