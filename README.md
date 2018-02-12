# Source Code Accompanying the Paper "More on Network Approaches in Historical Chinese Phonology"

This repository contains source code and data for the following paper:

* List, Johann-Mattis (2018): **More on network approaches in Historical Chinese Phonology (音韻學)**. Paper prepared for the *LFK Society Young Scholars Symposium*. Taibei: Li Fang-Kuei Society ofr Chinese Linguistics. URL: [https://hal.archives-ouvertes.fr/hal-01706927](https://hal.archives-ouvertes.fr/hal-01706927).

```bibtex
@InProceedings{List2018a,
  author      = {List, Johann-Mattis},
  title       = {{More on Network Approaches in Historical Chinese Phonology (音韻學)}},
  booktitle   = {{LFK Society Young Scholars Symposium}},
  year        = {2018},
  publisher   = {Li Fang-Kuei Society for Chinese Linguistics},
  pdf        = {https://hal.archives-ouvertes.fr/hal-01706927/file/main.pdf},
  url        = {https://hal.archives-ouvertes.fr/hal-01706927},
  address     = {Taipei},
  hal_id      = {hal-01706927},
}
```
 
## Requirements

- lingpy (http://lingpy.org)
- networkx (https://github.com/networkx/networkx)
- cytoscape (http://cytoscape.org, for exploring output graphs)
- SplitsTree (http://splitstree.org) to render the data-display networks

## Xíeshēng Networks

The folder `xiesheng` offers the following code, data, and additional files:

* `sinopy.py`: a little library offering a script needed for the computation 
* `karlgren1957.tsv': Karlgren's data on Grammata Serica Recensa, taken from the WikiBooks (see paper for details)
* `network.py`: main script which computes the network
* `xinsheng.tsv`: data from [CJKVI-IDS](https://github.com/cjkvi/cjkvi-ids) on the phonetic structure of characters
* `ab-groups.tsv': output produced by the algorithm, all groups in which third and first division are distinguished
* `graph-full.pdf`: full graph in PDF
* `graph-all.gml`: full graph in GML, can be read into cytoscape
* `web-session.zip`: Unzip the directory and open the file `index.html` in your browser to inspect the network interactively (exported thanks to Cytoscape)

To run the code, just make sure to have all dependencies installed (and that you use python3), and run:

```shell
$ python3 network.py
```

This will re-create the data (network, groups).

## Fǎnqiè Networks

The folder `guangyun` offers all data and files you need to replicate the study on fǎnqiè spellings mentioned in the paper.

- `guangyun.py`: main script to run the analysis
- `guangyun.tsv`: main data needed for the analysis
- `sinopy.py`: helper library
- `tls.json`: helper data for MC readings
- `guangyun.gml`: basic output (the network)
- `web-session.zip`: unpack and open `index.html` in browser for interactive inspection

To run this code, cd into the folder, and type:

```shell
$ python3 guangyun.py
```

## Evaluation 

Evaluation scripts can be found in the folder `evaluation`.

### Comparing Reconstruction Systems

The folder `evaluation` contains the following four files related to the comparison of reconstruction systems:

- `matrix.dst`: output of the algorithm, convenient to use in SplitsTree
- `reconstruction.py`: the code used to compute the network
- `reconstructions.tsv`: similar to `reconstructions.json` below, but different reconstructions
- `reconstructions.json`: eight different reconstructions for Old Chinese in json format (for a selected number of characters)


To run this code, cd into the folder, and type:

```shell
$ python3 reconstruction.py
```

### Comparing Rhyme Analyses

The folder `evaluation` also contains the data and code for the rhyme analyisis comparison.

- `Baxter1992.tsv`: rhyme annotation by Baxter (1992)
- `Wang1980.tsv`: rhyme annotation by Wáng (1980)
- `rhymes.py`: script that runs the comparison

To run this code, cd into the folder, and type:

```shell
$ python3 reconstruction.py
```


