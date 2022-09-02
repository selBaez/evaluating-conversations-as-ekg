# evaluating-conversations-as-ekg

Repository for experiments on evaluating the conversations modelled as episodic knowledge graphs, according to the @Leolani framework

## Overview

### Data overview

In the `data` folder you wil find a folder per conversation setup. Inside each folder there are several scenarios. The structure
of each scenario is the following:

| Folders                   | Description     |
| ------------------------- | :-------------- |
| \\{DATESTAMP}             | RDF .trig files per utterance that went in the brain |
| \\automatic_evaluations   | CSV file containing all proposed graph metrics and the aggregated human annotations and baseline automatic metrics |
| \\correlations            | CSV files containing correlations between automatic metrics, and human annotations |
| \\human_evaluations       | CSV files containing human annotations and baseline automatic metrics |
| \\plots                   | Plots for correlations and conversation flow |

### Code overview

In the `src` folder you will find the following:

| Folders                | Description                                                                              |
|------------------------|:-----------------------------------------------------------------------------------------|
| \\dialogue_creation    | Code to generate episodic knowledge graphs for human-human dialogues in the MELD dataset |
| \\dialogue_evaluations | Code to average and correlate human and automatic annotations                            |
| \\graph_evaluations    | Code to recreate conversations through RDF files, and compute metrics about the graphs   |

## Running the code

### Prerequisites

This repository uses Python >= 3.7. The following is the recommended set up for this project.

```
conda create --name evaluating-coversations-as-ekg python=3.7
conda activate evaluating-coversations-as-ekg
pip install --upgrade pip
pip install -r requirements.txt --no-cache
python -m ipykernel install --name=evaluating-coversations-as-ekg
```

### Reproducibility

To rerun the graph metric calculations, run `src/graph_evaluations/evaluate_rdf_scenarios.py` using one of the available configurations
in `resources/running_configs.txt`. To only recreate the plots, run `plot_rdf_scenarios.ipynb`.

## Authors

* [Selene Báez Santamaría](https://selbaez.github.io/)
* [Piek Vossen](https://github.com/piekvossen)
* [Thomas Baier](https://www.linkedin.com/in/thomas-baier-05519030/)
