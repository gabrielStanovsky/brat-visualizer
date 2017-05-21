import networkx as nx
from brat_handler import Brat


class NX_wrapper:
    """
    Simple wrapper for easier sentence level represenation
    """

    def __init__(self, sentence, word_indexed=True):
        """
        Initialize with a space separated sentence
        @:param word_indexed: boolean, indicating whether the indices used by add_edge function 
        are indices of words (True) or of character (False) 
        """
        self.sent = sentence
        self.graph = nx.DiGraph()
        self.word_indexed = word_indexed

    def add_edge(self, u, v, label):
        """
        Add a directed edge u -> v with a given label
        u and v should be 2-tuple of word indices indicating start and end
        i.e., u = (u_start, u_end), v = (v_start, v_end),
        """
        self.graph.add_edge(u, v)
        self.graph[u][v]['label'] = label.split(" ")

    def visualize(self, fn):
        """
        Visualize this structure into a brat html file
        """
        Brat.output_brat_html(self.sent,
                              self.graph,
                              fn,
                              self.word_indexed)

if __name__ == "__main__":
    ## Example usage

    # create instance with the sentence (words separated with space)
    g = NX_wrapper("the brown fox jumped over the lazy dog")

    # edges and labels
    g.add_edge((3, 4), (2, 3), "Who jumped?")
    g.add_edge((2, 3), (1, 2), "What color was the fox?")
    g.add_edge((3, 4), (7, 8), "Who did the fox jump over?")
    g.add_edge((6, 7), (7, 8), "Who was lazy?")

    # write visualizations to file
    g.visualize( "../visualizations/example.html")
