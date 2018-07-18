""" Usage:
    visualize_conll --in=INPUT_FILE --out=OUTPUT_FOLDER [--debug]

Writes an html file(s) with brat visualization of the input file, in CoNLL format.
Outputs are written in the output folder, one sentence per file.
"""
# External imports
import logging
from pprint import pprint
from pprint import pformat
from docopt import docopt
import networkx as nx
import os

# Local imports
from nx_wrapper import NX_wrapper
#=-----

def visualize_conll_sent(sent, fn):
    """
    Write an html representation of sent to fn.
    """
    logging.info(sent)

if __name__ == "__main__":
    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    out_folder = args["--out"]
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    # Process file
    sents = open(inp_fn).read().split('\n\n')

    logging.info("Processing {} sentences in {}".format(len(sents),
                                                        inp_fn))

    for sent_ind, sent in enumerate(sents):
        visualize_conll_sent(sent,
                             os.path.join(out_folder,
                                          "{}.html".format(sent_ind)))

    logging.info("DONE")
