# evaluating-coversations-as-ekg
Repository for experiments on evaluating the brain according to the @Leolani framework

## Getting started

### Prerequisites

This repository uses Python >= 3.7. The following is the recommended set up for this project.

```
conda create --name evaluating-coversations-as-ekg python=3.7
conda activate evaluating-coversations-as-ekg
pip install --upgrade pip
pip install -r requirements.txt --no-cache
python -m ipykernel install --name=evaluating-coversations-as-ekg

jupyter lab
```


Main scripts:
- folder called dialogue_evaluation is Piek's code to average and correlate human and automatic annotations
- folder called graph_evaluations is Selene's code to read RDF files, load them to a graph and compute metrics around it


TO DO:

- adapt script to chat with [Blenderbot](https://github.com/leolani/cltl-chatbots/blob/main/src/notebooks/conversation_between_dialogueGpt_and_Leolani.ipynb)


## Authors

* [Selene Báez Santamaría](https://selbaez.github.io/)
* [Thomas Baier](https://www.linkedin.com/in/thomas-baier-05519030/)
* [Piek Vossen](https://github.com/piekvossen)