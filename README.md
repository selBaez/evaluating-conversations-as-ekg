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
- [Lea - current] Look at the cltl-chatbots repo, follow install using requirements.txt  (use the old triple extractor so we can compare to student conversations)
- [Lea - next] Figure out bug
  in [Blenderbot](https://github.com/leolani/cltl-chatbots/blob/main/src/notebooks/conversation_between_dialogueGpt_and_Leolani.ipynb)
- Figure out bug
  in [DialogueGPT](https://github.com/leolani/cltl-chatbots/blob/main/src/notebooks/conversation_between_dialogueGpt_and_Leolani.ipynb)
- adapt [script](https://github.com/leolani/cltl-chatbots/blob/main/src/notebooks/lets-chat_with_a_brain_replier.ipynb)
  to chat with Blenderbot or DialogueGPT instead of user input. This script is a sample showing how to save data to
  EMISSOR and how to connect the CLTL packages
  
- Run [automatic evaluations](https://github.com/leolani/cltl-chatbots/blob/main/src/notebooks/dialogue_evaluation.ipynb) of Blenderbot or DialogueGPT conversations. This also saves them as csv with columns ready for human evaluation. 
- Run [graph evaluations](https://github.com/selBaez/evaluating-coversations-as-ekg/blob/main/src/graph_evaluations/evaluate_rdf_scenarios.py) of Blenderbot or DialogueGPT conversations


Notes for to do:
- Keep track of when you clear brain and when you continue on the same brain 

## Authors

* [Selene Báez Santamaría](https://selbaez.github.io/)
* [Piek Vossen](https://github.com/piekvossen)
* [Thomas Baier](https://www.linkedin.com/in/thomas-baier-05519030/)
