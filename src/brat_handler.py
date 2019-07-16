import json
import networkx as nx
from cgi import escape
import logging
import pdb
logging.basicConfig(level = logging.DEBUG)


class Brat:
    """
    Collections of brat handlers
    """

    @staticmethod
    def output_brat_html(sent, digraph, filename, brat_location, word_indexed=True):
        """
        Visualize the give digraph (networkx object) using brat
        output to the given filename.
        @param sent:  Space separated string
        @param digraph: Netowrkx object
        @param filename: file name in which to write the html code
        @param brat_location: path to the root of the brat installation to use
        @param word_indexed: boolean, indicating whether the indices in the digraph  
        are indices of words (True) or of characters (False)
        """
        split_sent = sent.split(' ')
        if word_indexed:
            get_character_span_of_node = lambda node: Brat.word_to_char(split_sent, node)
        else:   # node is already given in character-span format
            get_character_span_of_node = lambda node: node

        def toSentString(sentStr_or_lstOfWords):
            # handle both string labels and list-of-words labels
            if '__iter__' in dir(sentStr_or_lstOfWords):
                return " ".join(sentStr_or_lstOfWords)
            elif type(sentStr_or_lstOfWords) in (str, str):
                return sentStr_or_lstOfWords
            raise Exception("Parameter must be a string of an iterable of strings")

        entities = ",\n".join(["['A{0}_{1}', '', [[{0}, {1}]]]".format(char_start, char_end)
                               for char_start, char_end in map(get_character_span_of_node,
                                                               digraph.nodes())])
        rels = ",\n".join(["['R{}', '{}', [['head', '{}'], ['dep', '{}']]]".format(i,
                                                                                   label,
                                                                                   Brat.get_brat_name(src),
                                                                                   Brat.get_brat_name(dst))
                       for i, ((src, dst), label) in
                           enumerate([((get_character_span_of_node(source_dest_label[0]),
                                                                         get_character_span_of_node(source_dest_label[1])),
                                                                        escape(toSentString(source_dest_label[2]).replace("'", r"\'"))) for source_dest_label in [(source, dest, digraph[source][dest]["label"])
                                      for (source, dest) in digraph.edges()]])])

        brat_input = [(entities, rels)]
        html = Brat.get_brat_html(sent, brat_input, brat_location)

        with open(filename, 'w') as fout:
            fout.write(html)

        logging.debug("output written to: {}".format(filename))

    @staticmethod
    def word_to_char(sent, xxx_todo_changeme):
        """
        Given a tuple node indicating word start and end indices,
        return its corresponding char indices
        """
        (word_start, word_end) = xxx_todo_changeme
        word_end = word_end -1
        return (word_start + sum(map(len, sent[: word_start])),
                word_end + sum(map(len, sent[: word_end])) + len(sent[word_end]))

    @staticmethod
    def get_brat_name(node):
        """
        Get brat name for a given node
        """
        return "A{}_{}".format(*node)


    @staticmethod
    def get_brat_html(sent, graphs, brat_location):
        """
        Return a brat html text of graphs (list of entities and relations
        sent is a string representing the sentence
        """
        docdata = "\n".join([Brat.brat_template.replace("SENTENCE_STUB",
                                                        sent).\
                             replace("ENTITIES_STUB",
                                     entities).\
                             replace("RELATIONS_STUB",
                                     rels).\
                             replace("LABEL_NUM_STUB",
                                     str(graph_ind))
                             for graph_ind, (entities, rels) in enumerate(graphs)])


        embedding = "\n".join([Brat.embedding_template.replace("LABEL_NUM_STUB", str(i))
                               for i in range(len(graphs))])

        div = "\n".join([Brat.div_template.replace("LABEL_NUM_STUB", str(i))
                               for i in range(len(graphs))])


        return Brat.html_template.replace("DOCDATA_STUB", docdata).\
            replace("EMBEDDING_STUB", embedding).\
            replace("DIV_STUB", div).\
            replace("BRAT_LOCATION_STUB",
                    brat_location)



    brat_template = """
    var docData_LABEL_NUM_STUB = { text: "SENTENCE_STUB",

    entities: [

    ENTITIES_STUB

    ],

    relations: [

    RELATIONS_STUB

    ]
    };

    """

    embedding_template = """
        Util.embed(
        // id of the div element where brat should embed the visualisations
        'label_LABEL_NUM_STUB',
        // object containing collection data
        collData,
        // object containing document data
        docData_LABEL_NUM_STUB,
        // Array containing locations of the visualisation fonts
        webFontURLs
        );
    """

    div_template = """
    <div id="label_LABEL_NUM_STUB"></div>
    <br><br>
    """

    html_template = """
    <html>
 <head>
   <link rel="stylesheet" type="text/css" href="BRAT_LOCATION_STUB/style-vis.css"/>
   <script type="text/javascript" src="BRAT_LOCATION_STUB/client/lib/head.load.min.js"></script>
</head>
<body>


    <script language="javascript">

    var bratLocation = 'BRAT_LOCATION_STUB/';
head.js(
    // External libraries
    bratLocation + '/client/lib/jquery.min.js',
    bratLocation + '/client/lib/jquery.svg.min.js',
    bratLocation + '/client/lib/jquery.svgdom.min.js',

    // brat helper modules
    bratLocation + '/client/src/configuration.js',
    bratLocation + '/client/src/util.js',
    bratLocation + '/client/src/annotation_log.js',
    bratLocation + '/client/lib/webfont.js',

    // brat modules
    bratLocation + '/client/src/dispatcher.js',
    bratLocation + '/client/src/url_monitor.js',
    bratLocation + '/client/src/visualizer.js'
    );

    var webFontURLs = [
    bratLocation + '/static/fonts/Astloch-Bold.ttf',
    bratLocation + '/static/fonts/PT_Sans-Caption-Web-Regular.ttf',
    bratLocation + '/static/fonts/Liberation_Sans-Regular.ttf'
    ];


    var collData = {

    entity_types: [ {
            type   : 'Predicate',
            labels : ['Predicate', 'Pr'],
            bgColor: '#7fa2ff',
            borderColor: 'darken'
    },
    {
            type   : 'Argument',
            labels : ['Argument', 'Ar'],
            bgColor: '#ff6a36',
            borderColor: 'darken'
    },
]
    };




    DOCDATA_STUB


     head.ready(function() {
    EMBEDDING_STUB

});

  </script>

    DIV_STUB


</body>
</html>
"""
