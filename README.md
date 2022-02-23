# evaluating-coversations-as-ekg
Repository for experiments on evaluating the brain accordingto the @Leolani framework


```
conda create --name evaluating-coversations-as-ekg python=3.7
conda activate evaluating-coversations-as-ekg
pip install --upgrade pip
pip install -r requirements.txt --no-cache
python -m ipykernel install --name=evaluating-coversations-as-ekg

jupyter lab
```


Main scripts:
- folder called dialogue_evaluation is Piek's code to average and correlate human annotations
- folder called graph_evaluations is Selene's code to read RDF files, load them to a graph and compute metrics about it


Notes
- I have been working first with G1Piek thomas conversation as a trial

TO DO:

- adapt script to chat with [Blenderbot](https://github.com/leolani/cltl-chatbots/blob/main/src/notebooks/conversation_between_dialogueGpt_and_Leolani.ipynb) 
- average 