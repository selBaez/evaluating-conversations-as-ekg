"""
NOTES
TO DO: compare extraction now with rdf files in log, extract main claim
"""

import os
import time
from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from cltl.brain.long_term_memory import LongTermMemory

ABSOLUTE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = ABSOLUTE_PATH + f'/../../data/g1-piek/scenario1/'
INPUT_FOLDER = DATA_FOLDER + f'human_evaluations/'
RDF_FOLDER = DATA_FOLDER + f'2021-12-07-16_26_14/rdf/2021-12-07-16-26/'
OUTPUT_FOLDER = DATA_FOLDER + f'automatic_evaluations/'

CONVOS_FILES = [
    '2021-12-07-16_26_14_turns83_thomas-copy.csv',
    # '2021-12-07-16_26_14_turns83_thomas.csv',
    # '2021-12-07-16-26-14_truns83_imme.csv',
    # '2021-12-07-16-26-14_turns83_fina.csv'
]


def save(file_num, df):
    # select relevant columns to plot
    df = df[['Turn', 'Speaker',
             'System llh', 'MLM llh', 'USR DLcontext', 'USR DLfact',
             'Overall Human Rating', 'Interesting', 'Engaging', 'Specific', 'Relevant',
             'Correct', 'Semantically Appropriate', 'Understandable', 'Fluent',
             'Total explicit triples', 'Total semantic statements', 'Total sources',
             'Total predicates', 'Total classes']]
    df.to_csv(OUTPUT_FOLDER + f'{file_num}.csv', index=False)


def evaluate_conversation(convos_files):
    # Read separate file with rdf_file column but no human evaluations

    # Read list of human evaluations (3 in this case)
    # For each, gather the columns and name th

    # 'Overall Human Rating' 'Interesting' 'Engaging' 'Specific' 'Relevant',
    # 'Correct' 'Semantically Appropriate' 'Understandable' 'Fluent',

    # Brain object in Python, fresh Dataset
    brain = LongTermMemory(address="http://localhost:7200/repositories/evaluating-conversations",
                           log_dir=Path("../logs"),
                           clear_all=True)

    for file_num, file in enumerate(convos_files):
        # Read CSV with pandas
        df = pd.read_csv(INPUT_FOLDER + file, header=0, sep=';')

        # Create placeholders
        df["Total explicit triples"] = np.nan
        df["Total semantic statements"] = np.nan
        df["Total sources"] = np.nan
        df["Total predicates"] = np.nan
        df["Total classes"] = np.nan
        rdf_count = 0
        response_code = ''

        # Iterate through turns
        for idx, row in df.iterrows():
            print(f"Processing turn {row['Turn']}")

            # if row has a file to rdf, process it
            if type(row['rdf_file']) == str:
                # Update count
                rdf_count += 1
                print(f"\tAdding RDF, cumulative: {rdf_count}")

                # clear brain (for comutational purposes)
                print(f"\tClear Long and short term memory")
                brain.clear_brain()
                brain.assign_local_memory()

                # Add new
                brain.dataset.parse(RDF_FOLDER + row['rdf_file'], format='trig')
                data = brain.dataset.serialize(format=brain._connection.format)

                print(f"\tGiving the triple store some time")
                start = time.time()
                response_code = brain._upload_to_brain(data)
                stop = time.time()
                print(f"\tTotal time for upload: {timedelta(seconds=stop - start)}")

            # metrics as columns
            print(f"\tCalculating brain metrics")
            df.loc[idx, 'Total explicit triples'] = len(brain.dataset)
            df.loc[idx, 'Total semantic statements'] = brain.count_statements()
            df.loc[idx, 'Total sources'] = brain.count_friends()
            df.loc[idx, 'Total predicates'] = len(brain.get_predicates())
            df.loc[idx, 'Total classes'] = len(brain.get_classes())
            # 'cardinality conflicts': len(thoughts.complement_conflicts()),
            # 'negation conflicts': len(thoughts.negation_conflicts()),
            # 'subject gaps': len(thoughts.subject_gaps()),
            # 'object gaps': len(thoughts.complement_gaps()),
            # 'statement novelty': len(thoughts.statement_novelties()),
            # 'subject novelty': thoughts.entity_novelty().subject,
            # 'object novelty': thoughts.entity_novelty().complement,
            # 'overlaps subject-predicate': len(thoughts.overlaps().subject),
            # 'overlaps on predicate-object': len(thoughts.overlaps().complement),
            # 'trust': thoughts.trust(),

            # Report
            if type(row['Overall Human Rating']) == float:
                evals = row[['Overall Human Rating',
                             'Interesting', 'Engaging', 'Specific', 'Relevant', 'Correct',
                             'Semantically Appropriate', 'Understandable', 'Fluent',
                             'Total explicit triples', 'Total semantic statements', 'Total sources',
                             'Total predicates', 'Total classes']].values

                print(f"\tEvaluations: {evals} ")

            # if idx == 3:
            #     break

        save(file_num, df)


if __name__ == "__main__":
    evaluate_conversation(CONVOS_FILES)

    print('ALL DONE')
