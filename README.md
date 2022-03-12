# evaluating-coversations-as-ekg

Repository for experiments on evaluating the brain according to the @Leolani framework

## Overview

### Data overview

In the `data` folder you wil find a folder per student group. Inside each group there are two scenarios. The structure
of each scenario is the following:

| Folders                   | Description     |
| ------------------------- | :-------------- |
| \\{DATESTAMP}             | RDF .trig files per utterance that went in the brain |
| \\automatic_evaluations   | CSV file containing all automatic metrics, graph metrics and the aggregated human annotations |
| \\correlations            | CSV files containing correlations between automatic metrics, and human annotations |
| \\human_evaluations       | CSV files containing all automatic metrics, and human annotations |
| \\plots                   | Plots for correlations and conversation flow |

### Code overview

In the `src` folder you will find the following:

| Folders                   | Description     |
| ------------------------- | :-------------- |
| \\dialogue_evaluations     | Code to average and correlate human and automatic annotations |
| \\graph_evaluations       | Code to recreate conversations through RDF files, and compute metrics about the graphs |

To rerun the graph metric calculations, run `evaluate_rdf_scenarios.py` using one of the available configurations
in `resources/running_configs.txt`. To only recreate the plots, run `plot_rdf_scenarios.ipynb`.

## Getting started

### Prerequisites

This repository uses Python >= 3.7. The following is the recommended set up for this project.

```
conda create --name evaluating-coversations-as-ekg python=3.7
conda activate evaluating-coversations-as-ekg
pip install --upgrade pip
pip install -r requirements.txt --no-cache
python -m ipykernel install --name=evaluating-coversations-as-ekg
```

[comment]: <> (TO DO:)

[comment]: <> (- [Lea - done] Look at the cltl-chatbots repo, follow install using requirements.txt  &#40;use the old triple extractor so)

[comment]: <> (  we can compare to student conversations&#41;)

[comment]: <> (- [Lea - done] Figure out bug)

[comment]: <> (  in [Blenderbot]&#40;https://github.com/leolani/cltl-chatbots/blob/main/src/notebooks/conversation_between_dialogueGpt_and_Leolani.ipynb&#41;)

[comment]: <> (- [Lea - current] Figure out bug)

[comment]: <> (  in [DialogueGPT]&#40;https://github.com/leolani/cltl-chatbots/blob/main/src/notebooks/conversation_between_dialogueGpt_and_Leolani.ipynb&#41;)

[comment]: <> (TO ASSIGN:)

[comment]: <> (- Adapt [script]&#40;https://github.com/leolani/cltl-chatbots/blob/main/src/notebooks/lets-chat_with_a_brain_replier.ipynb&#41;)

[comment]: <> (  to chat with Blenderbot or DialogueGPT instead of user input. This script is a sample showing how to save data to)

[comment]: <> (  EMISSOR and how to connect the CLTL packages)

[comment]: <> (- Run automatic evaluations of Blenderbot or DialogueGPT conversations. This also saves them as csv with columns ready)

[comment]: <> (  for human evaluation.)

[comment]: <> (- Run graph evaluations of Blenderbot or DialogueGPT conversations)

[comment]: <> (Notes for to do:)

[comment]: <> (- Keep track of when you clear brain and when you continue on the same brain)

## Authors

* [Selene Báez Santamaría](https://selbaez.github.io/)
* [Piek Vossen](https://github.com/piekvossen)
* [Thomas Baier](https://www.linkedin.com/in/thomas-baier-05519030/)
