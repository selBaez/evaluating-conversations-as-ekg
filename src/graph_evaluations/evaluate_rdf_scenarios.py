"""
NOTES
TO DO: compare extraction now with rdf files in log, extract main claim
"""

import os

import pandas as pd
from rdflib import Dataset, ConjunctiveGraph
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph

from src.graph_evaluations.metrics.graph_measures import *
from src.graph_evaluations.metrics.ontology_measures import *

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
    # df = df[['Turn', 'Speaker',
    #          'System llh', 'MLM llh', 'USR DLcontext', 'USR DLfact',
    #          'Overall Human Rating', 'Interesting', 'Engaging', 'Specific', 'Relevant',
    #          'Correct', 'Semantically Appropriate', 'Understandable', 'Fluent',
    #          'Total explicit triples', 'Total semantic statements', 'Total sources',
    #          'Total predicates', 'Total classes']]
    df.to_csv(OUTPUT_FOLDER + f'{file_num}_nobrain.csv', index=False)


def evaluate_conversation(convos_files):
    # Read separate file with rdf_file column but no human evaluations

    # Read list of human evaluations (3 in this case)
    # For each, gather the columns and name th

    # 'Overall Human Rating' 'Interesting' 'Engaging' 'Specific' 'Relevant',
    # 'Correct' 'Semantically Appropriate' 'Understandable' 'Fluent',

    # Brain object in Python, fresh Dataset
    brain = Dataset()
    brain_as_graph = ConjunctiveGraph()
    brain_as_netx = rdflib_to_networkx_multidigraph(brain_as_graph)

    for file_num, file in enumerate(convos_files):
        # Read CSV with pandas
        df = pd.read_csv(INPUT_FOLDER + file, header=0, sep=';')

        # Create placeholders
        rdf_count = 0

        # Iterate through turns
        for idx, row in df.iterrows():
            print(f"Processing turn {row['Turn']}")

            # if row has a file to rdf, process it
            if type(row['rdf_file']) == str:
                # Update count
                rdf_count += 1
                print(f"\tFound RDF, cumulative: {rdf_count}")

                # clear brain (for computational purposes)
                print(f"\tClear Long and short term memory")
                brain = Dataset()
                brain_as_graph = ConjunctiveGraph()

                # Add new
                print(f"\tAdding triples to brains")
                brain.parse(RDF_FOLDER + row['rdf_file'], format='trig')
                brain_as_graph.parse(RDF_FOLDER + row['rdf_file'], format='trig')
                brain_as_netx = rdflib_to_networkx_multidigraph(brain_as_graph)

            # metrics as columns (only when needed! otherwise copy row)
            print(f"\tCalculating brain metrics")
            df.loc[idx, 'Total nodes'] = get_count_nodes(brain_as_netx)
            df.loc[idx, 'Total edges'] = get_count_edges(brain_as_netx)
            df.loc[idx, 'Average degree'] = get_avg_degree(brain_as_netx)
            df.loc[idx, 'Average degree centrality'] = get_avg_degree_centr(brain_as_netx)
            df.loc[idx, 'Average closeness'] = get_avg_closeness(brain_as_netx)
            # df.loc[idx, 'Average betweenness'] = get_avg_betweenness(brain_as_netx)
            df.loc[idx, 'Average degree connectivity'] = get_degree_connectivity(brain_as_netx)
            df.loc[idx, 'Average assortativity'] = get_assortativity(brain_as_netx)
            df.loc[idx, 'Average node connectivity'] = get_node_connectivity(brain_as_netx)
            df.loc[idx, 'Number of components'] = get_number_components(brain_as_netx)
            df.loc[idx, 'Number of strong components'] = get_assortativity(brain_as_netx)
            # df.loc[idx, 'Shortest path'] = get_shortest_path(brain_as_netx)
            df.loc[idx, 'Centrality entropy'] = get_entropy_centr(brain_as_netx)
            df.loc[idx, 'Closeness entropy'] = get_shortest_path(brain_as_netx)
            df.loc[idx, 'Sparseness'] = get_sparseness(brain_as_netx)
            ####
            df.loc[idx, 'Total explicit triples'] = len(brain)
            df.loc[idx, 'Total properties'] = get_number_properties(brain_as_graph)
            df.loc[idx, 'Total classes'] = get_number_classes(brain_as_graph)
            #####
            df.loc[idx, 'Total semantic statements'] = ''
            df.loc[idx, 'Total sources'] = ''

            # Report
            if row['Overall Human Rating'] is not np.nan:
                evals = df.loc[idx, ['Overall Human Rating',
                                     'Interesting', 'Engaging', 'Specific', 'Relevant', 'Correct',
                                     'Semantically Appropriate', 'Understandable', 'Fluent',
                                     'Total explicit triples', 'Total semantic statements', 'Total sources',
                                     'Total predicates', 'Total classes']].values

                print(f"\tEvaluations: {evals} ")

            # if idx == 3:
            #     break

        save(file_num, df)

        return df


if __name__ == "__main__":
    df = evaluate_conversation(CONVOS_FILES)

    print('ALL DONE')
