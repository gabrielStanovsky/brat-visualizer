import json
import networkx as nx
from cgi import escape
import logging
logging.basicConfig(level = logging.DEBUG)


class Brat:
    """
    Collections of brat handlers
    """

    @staticmethod
    def output_brat_html(sent, digraph, filename):
        """
        Visualize the give digraph (networkx object) using brat
        output to the given fileaname.
        @param sent:  Space separated string
        @param digraph: Netowrkx object
        @param filename: file name in which to write the html code
        """
        split_sent = sent.split(' ')
        entities = ",\n".join(["['A{0}_{1}', '', [[{0}, {1}]]]".format(char_start, char_end)
                               for char_start, char_end in map(lambda n: Brat.word_to_char(split_sent,
                                                                                      n),
                                                               digraph.nodes())])
        rels = ",\n".join(["['R{}', '{}', [['head', '{}'], ['dep', '{}']]]".format(i,
                                                                                   label,
                                                                                   Brat.get_brat_name(src),
                                                                                   Brat.get_brat_name(dst))
                       for i, ((src, dst), label) in
                           enumerate(map(lambda (source, dest, label): ((Brat.word_to_char(split_sent,
                                                                                      source),
                                                                         Brat.word_to_char(split_sent,
                                                                                      dest)),
                                                                        escape(" ".join(label).replace("'", r"\'"))),
                                         [(source, dest, digraph[source][dest]["label"])
                                      for (source, dest) in digraph.edges()]
                           ))])

        brat_input = [(entities, rels)]
        html = Brat.get_brat_html(sent, brat_input)

        with open(filename, 'w') as fout:
            fout.write(html)

        logging.debug("output written to: {}".format(filename))

    @staticmethod
    def word_to_char(sent, (word_start, word_end)):
        """
        Given a tuple node indicating word start and end indices,
        return its corresponding char indices
        """
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
    def get_brat_html(sent, graphs):
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
            replace("DIV_STUB", div)


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




#     {

#     // Our text of choice
#     text     : "It is the text of a speech given by an Arab gentleman before the advisory board of a large multi-nation corporation .",
#     // The entities entry holds all entity annotations
#     entities : [
#         /* Format: [${ID}, ${TYPE}, [[${START}, ${END}]]]
#             note that range of the offsets are [${START},${END})
#         ['T1', 'Predicate', [[0, 11]]],
#         ['T2', 'Predicate', [[20, 23]]],
#         ['T3', 'Predicate', [[37, 40]]],
#     ['T4', 'Predicate', [[50, 61]]], */
#       ['A27_32', '', [[27, 32]]],
# ['A20_26', '', [[20, 26]]],
# ['A74_79', '', [[74, 79]]],
# ['A44_53', '', [[44, 53]]],
# ['A85_90', '', [[85, 90]]],
# ['A65_73', '', [[65, 73]]],
# ['A39_43', '', [[39, 43]]],
# ['A91_115', '', [[91, 115]]],
# ['A10_14', '', [[10, 14]]]
#     ],

#     };



# docData['relations'] = [
#     // Format: [${ID}, ${TYPE}, [[${ARGNAME}, ${TARGET}], [${ARGNAME}, ${TARGET}]]]
# /*    ['R1', 'Who said something?', [['dep', 'T2'], ['head', 'T1']]] */
#       ['R0', 'Who gave this speech ?', [['head', 'A27_32'], ['dep', 'A44_53']]],
# ['R1', 'who did he give the speech in front of ?', [['head', 'A27_32'], ['dep', 'A74_79']]],
# ['R2', 'Who gave this speech ?', [['head', 'A27_32'], ['dep', 'A20_26']]],
# ['R3', 'Who read out this speech text ?', [['head', 'A20_26'], ['dep', 'A10_14']]],
# ['R4', 'What kind of board is it ?', [['head', 'A74_79'], ['dep', 'A65_73']]],
# ['R5', 'What kind of corporation was the board for ?', [['head', 'A74_79'], ['dep', 'A91_115']]],
# ['R6', 'what nationality is this gentleman ?', [['head', 'A44_53'], ['dep', 'A39_43']]],
# ['R7', 'What size is the multi-nation corporation ?', [['head', 'A91_115'], ['dep', 'A85_90']]]
#     ];
# """

    html_template = """
    <html>
 <head>
   <link rel="stylesheet" type="text/css" href="./brat/style-vis.css"/>
   <script type="text/javascript" src="./brat/client/lib/head.load.min.js"></script>
</head>
<body>


    <script language="javascript">

    var bratLocation = './brat';
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

if __name__ == "__main__":
    # Example usage
    sent = "the brown fox jumped over the lazy dog"
    g = nx.DiGraph()
    # edges and labels
    g.add_edge((3, 4), (2, 3))
    g[(3, 4)][(2, 3)]['label'] = "Who jumped?".split(" ")
    Brat.output_brat_html(sent, g, "../visualizations/example.html")
