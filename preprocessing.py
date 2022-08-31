"""
Script to preprocess input file

- Remove special characters
- Everything lower case
"""

import argparse
import os

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()

    parser.add_argument("input", type=str,
            help="""Message to encode.
            - If a file exists, then open and read the file.
            - If no path exists, consider this input as the message to encode.""")

    parser.add_argument("--save_path", type=str,
            default="corpus/",
            help="Folder to save the file. Name would be the same as input, so do not select the same folder.")

    args = parser.parse_args()


    assert(os.path.exists(args.input))
    os.makedirs(args.save_path, exist_ok=True)


    data = None
    with open(args.input, "r") as fp:
        data = fp.read().lower()

    print("Read {} characters".format(len(data)))
    
    # Remove special characters
    for c in "\"&#'}{()[]-|è`_\\^@=$£%µ*!:.;,?/↑":
        data = data.replace(c, " ")
    
    print("After special char remova {} characters".format(len(data)))
    
    # Remove empty lines
    data = data.split('\n')
    print("Found {} lines".format(len(data)))
    clean = []
    for row in data:
        if "http" in row:
            continue
        elif "www" in row:
            continue
        elif len(row) < 30:
            continue
        else:
            # Transform n-space into 1-space 
            clean.append(" ".join(row.split()))
    
    print("Valid  {} lines".format(len(clean)))

    with open("{}{}".format(args.save_path, args.input.rsplit("/", 1)[-1]), "w") as fp:
        fp.write("\n".join(clean))

