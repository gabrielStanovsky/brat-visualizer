"""
Common functions for reading sdp format.
"""
# External imports
import logging
import pdb
from pprint import pprint
from pprint import pformat
from docopt import docopt
import networkx as nx
#import matplotlib.pyplot as plt

# Local imports


#----

def safe_zip(*lists):
    """
    Zip while making sure all lists are of same
    length.
    """
    if lists:
        assert(all([len(lists[0]) == len(ls)
                    for ls in lists[1:]]))
    return zip(*lists)


def get_words_and_preds(sdp_lines):
    """
    Returns the words in the lines, split to columns.
    and the predicates (subset of words).
    """
    words = [line.strip().split("\t")
             for line in sdp_lines
             if (not line.startswith('#')) and \
             line.strip()]
    preds = [word
             for word in words
             if word[5] == '+']
    return (words, preds)


def get_nx_graph(sdp_lines, remove_singletons = False):
    """
    Return a networkx graph representation of the conll
    input.
    @param remove_singletons: Indicates whether to remove nodes which
                              aren't connected to any other node.
    """
    graph = nx.MultiDiGraph()
    words, preds = get_words_and_preds(sdp_lines)
    total_rels = 0
    err_cnt = 0
    for line in words:
        cur_ind = int(line[0]) - 1
        graph.add_node(cur_ind,
                       label =  "{}_{}".format(cur_ind, line[1]),
                       word = line[1])
        rels = line[7:]
        active_rels = [(rel_ind, rel)
                       for rel_ind, rel in enumerate(rels)
                       if rel != "_"]
        total_rels += len(active_rels)
        for pred_ref, rel in active_rels:
            # populate graph with relations
            pred_ind = int(preds[pred_ref][0]) - 1
            graph.add_edge(pred_ind,
                           cur_ind,
                           label = rel)

    if remove_singletons:
        nodes_to_remove = []
        for node in graph.nodes():
            if not (nx.descendants(graph, node) or nx.ancestors(graph, node)):
                nodes_to_remove.append(node)

        for node in nodes_to_remove:
            graph.remove_node(node)

    return graph

def draw_graph(graph):
    """
    Draw the given graph.
    """
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,
                           pos,
                           node_color = 'w',
                           linewidths = 0,
                           node_size = 1500,
                           node_shape = 's')

    nx.draw_networkx_labels(graph,
                            pos,
                            labels = nx.get_node_attributes(graph,
                                                            'word'))

    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_edge_labels(graph,
                                 pos,
                                 edge_labels = nx.get_edge_attributes(graph,
                                                                      'label'))
    plt.show()


def get_outgoing_edges(graph, node):
    """
    Get all outgoing edges from a given node in
    a graph.
    Includes logic for choosing the ordering of the edges.
    """
    return [(node, neighbor, edge_key)
            for neighbor, edge_keys
            in graph[node].iteritems()
            for edge_key in edge_keys]
