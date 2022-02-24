import os

import numpy as np
import pandas as pd

ABSOLUTE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = ABSOLUTE_PATH + f'/../../data/g1-piek/scenario1/'
SCENARIO_FOLDER = DATA_FOLDER + f'2021-12-07-16_26_14/'
INPUT_FOLDER = DATA_FOLDER + f'human_evaluations/'

if __name__ == "__main__":
    # Little script in case we need to manually map rdf files to turns
    temp_df = pd.read_csv(INPUT_FOLDER + '2021-12-10-09_35_57_turns57_thomas.csv')
    temp_df['rdf_file'] = np.nan
    temp_df = temp_df[['Turn', 'Speaker', 'Response', 'rdf_file']]
    js = temp_df.to_json(orient='records')
    with open(SCENARIO_FOLDER + '/turn_to_trig_file.json', 'w') as f:
        f.write(js)
