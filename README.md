# Brat Visualizer 

Visualize graphs over sentences using the [brat framework](http://brat.nlplab.org/index.html).

## Install
`pip install -r requirements`

## Visualize SDP
From the `src` folder, run:

```
python visualize_sdp.py --in=<SDP-FILE> --brat=<BRAT-ROOT> --out=<OUTPUT-FOLDER>
```


For example, try:

```sh
python visualize_sdp.py --in=./sdp_sample.conll --brat=../brat/brat-v1.3_Crunchy_Frog --out=../visualizations
```

### Output
Should be created in the given output folder, one sentence per file, and an additional `index.html` file with links to all generated structures.
