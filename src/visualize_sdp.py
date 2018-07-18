""" Usage:
    <file-name> --in=INPUT_FILE --brat=BRAT_LOCATION --out=OUTPUT_FOLDER [--debug]

Get dot files for each graph in a given input file.

"""
# External imports
import logging
import pdb
import os
from pprint import pprint
from pprint import pformat
from docopt import docopt
from networkx.drawing.nx_agraph import write_dot
from operator import itemgetter
import networkx as nx


# Local imports
from sdp_readers import get_nx_graph
from nx_wrapper import NX_wrapper
#----

# Change default encoding to UTF8 to avoid handling.
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


if __name__ == "__main__":

    # Parse command line arguments
    args = docopt(__doc__)
    inp_fn = args["--in"]
    brat_location = os.path.abspath(args["--brat"])
    out_fn = args["--out"]

    # Determine logging level
    debug = args["--debug"]
    if debug:
        logging.basicConfig(level = logging.DEBUG)
    else:
        logging.basicConfig(level = logging.INFO)

    # Start computation
    graphs = [get_nx_graph(lines.split("\n"), remove_singletons = False)
              for lines in
              open(inp_fn).read().decode("utf8").split("\n\n")
              if lines.strip()]

    index = []

    for sent_ind, graph in enumerate(graphs):
        sent = ' '.join(map(itemgetter('word'),
                            graph.nodes().values()))
        conll = NX_wrapper(sent, brat_location)

        # Add edges
        for (u, v) in nx.edges(graph):
            edges = graph[u][v]

            # No more than one relation per two nodes
            assert(len(edges) == 1)

            # Add edge
            label = graph[u][v][0]['label']
            conll.add_edge((u, u + 1),
                       (v, v + 1),
                       label)

        # Write to file and record index
        cur_fn = "{}.html".format(sent_ind)
        index.append((sent, cur_fn))

        conll.visualize(os.path.join(out_fn,
                                     cur_fn))

    # Write index file
    index_fn = os.path.join(out_fn,
                            "index.html")
    logging.info("Writing index file to {}".format(index_fn))

    with open(index_fn,'w') as fout:
        fout.write('<br>\n'.join(["<a href={}>{}</a>".format(link,
                                                             sent)
                                for (sent, link)
                                in index]))

    # End
    logging.info("DONE")
