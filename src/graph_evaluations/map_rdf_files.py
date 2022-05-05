import json
import os
from pathlib import Path

import pandas as pd

ABSOLUTE_PATH = os.path.dirname(os.path.realpath(__file__))
HUMAN_EVAL = False
DATA_FOLDER = ABSOLUTE_PATH + f'/../../data/e2-blender_eliza_spacy/scenario1/'
SCENARIO_FOLDER = DATA_FOLDER + f'2022-05-03-19_43_11/'
RDF_FOLDER = SCENARIO_FOLDER + f'rdf/2022-05-03-19-44/'
INPUT_FOLDER = DATA_FOLDER + f'human_evaluations/'


def map_student_evaluations():
    # Reconstruct from csv with utterances
    temp_df = pd.read_csv(INPUT_FOLDER + 'Fajjaaz - 2 - 2021-12-10-09_23_53_turns10_context300.csv')
    temp_df['rdf_file'] = []
    temp_df = temp_df[['Turn', 'Speaker', 'Response', 'rdf_file']]
    js = temp_df.to_json(orient='records')
    with open(SCENARIO_FOLDER + '/turn_to_trig_file.json', 'w') as f:
        f.write(js)


def map_emissor_scenarios():
    # Read rdf files
    datapath = Path(RDF_FOLDER)
    files = sorted([path for path in datapath.glob('*.trig')])

    # Reconstruct from EMISSOR
    with open(SCENARIO_FOLDER + 'text.json', 'r') as j:
        data = json.loads(j.read())

    utterances = []
    utt_id = None

    for index, item in enumerate(data):
        speakers = set()
        rdf_file = []

        for m in item['mentions']:
            for ann in m['annotations']:
                if type(ann) == list:
                    ann = ann[0]
                if ann['type'] == 'utterance':
                    speakers.add(ann['source'])
                    utt_id = ann['value']

        # find in files
        if utt_id:
            for f in files:
                txt = Path(f).read_text()
                if utt_id in txt:
                    rdf_file = [f.stem + '.trig']
                    files.remove(f)
                    break

        utterance = {"Turn": index, "Speaker": speakers.pop(),
                     "Response": ''.join(item['seq']), "rdf_file": rdf_file}
        utterances.append(utterance)

    with open(SCENARIO_FOLDER + '/turn_to_trig_file.json', 'w') as f:
        js = json.dumps(utterances)
        f.write(js)


if __name__ == "__main__":
    # Little script in case we need to manually map rdf files to turns

    if HUMAN_EVAL:
        map_student_evaluations()

    else:
        map_emissor_scenarios()
