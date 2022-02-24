"""
NOTES
TO DO: compare extraction now with rdf files in log, extract main claim
"""

import os
from pathlib import Path

import pandas as pd
from rdflib import Dataset, ConjunctiveGraph, URIRef
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
from rdflib.namespace import FOAF, RDF

from src.graph_evaluations.metrics.graph_measures import *
from src.graph_evaluations.metrics.ontology_measures import *

ABSOLUTE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = ABSOLUTE_PATH + f'/../../data/g1-piek/scenario2/'
SCENARIO_FOLDER = DATA_FOLDER + f'2021-12-10-09_35_57/'
RDF_FOLDER = SCENARIO_FOLDER + f'rdf/2021-12-10-09-36/'
INPUT_FOLDER = DATA_FOLDER + f'human_evaluations/'
OUTPUT_FOLDER = DATA_FOLDER + f'automatic_evaluations/'


def save(file_num, df):
    df = df.drop(columns=['Speaker', 'Response', 'rdf_file'])
    df.to_csv(OUTPUT_FOLDER + f'{file_num}.csv', index=False)


def calculate_metrics(brain, brain_as_graph, brain_as_netx, df, idx):
    print(f"\tCalculating graph metrics")
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
    print(f"\tCalculating RDF graph metrics")
    df.loc[idx, 'Total explicit triples'] = len(brain)
    df.loc[idx, 'Total classes'] = get_number_classes(brain_as_graph)
    df.loc[idx, 'Total properties'] = get_number_properties(brain_as_graph)
    df.loc[idx, 'Total instances'] = get_number_instances(brain_as_graph)
    df.loc[idx, 'Total object properties'] = get_number_properties_object(brain_as_graph)
    df.loc[idx, 'Total data properties'] = get_number_properties_datatype(brain_as_graph)
    df.loc[idx, 'Total equivalent class properties'] = get_number_properties_equivClass(brain_as_graph)
    df.loc[idx, 'Total subclass properties'] = get_number_properties_subclass(brain_as_graph)
    df.loc[idx, 'Total entities'] = get_number_entities(brain_as_graph)
    df.loc[idx, 'Total inverse entities'] = get_number_inverse(brain_as_graph)
    df.loc[idx, 'Ratio of inverse relations'] = get_ratio_inverse_relations(brain_as_graph)
    df.loc[idx, 'Property class ratio'] = get_property_class_ratio(brain_as_graph)
    df.loc[idx, 'Average population'] = get_avg_population(brain_as_graph)
    df.loc[idx, 'Class property ratio'] = get_class_property_ratio(brain_as_graph)
    df.loc[idx, 'Attribute richness'] = get_attribute_richness(brain_as_graph)
    df.loc[idx, 'Inheritance richness'] = get_inheritance_richness(brain_as_graph)
    df.loc[idx, 'Relationship richness'] = get_relationship_richness(brain_as_graph)
    df.loc[idx, 'Object properties ratio'] = get_ratio_object_properties(brain_as_graph)
    df.loc[idx, 'Datatype properties ratio'] = get_ratio_datatype_properties(brain_as_graph)
    df.loc[idx, 'Total concept assertions'] = get_number_concept_assertions(brain_as_graph)
    df.loc[idx, 'Total role assertions'] = get_number_role_assertions(brain_as_graph)
    df.loc[idx, 'Total general concept inclusions'] = get_number_GCI(brain_as_graph)
    df.loc[idx, 'Total domain axioms'] = get_number_domain_axioms(brain_as_graph)
    df.loc[idx, 'Total range axioms'] = get_number_range_axioms(brain_as_graph)
    df.loc[idx, 'Total role inclusions'] = get_number_role_inclusion(brain_as_graph)
    df.loc[idx, 'Total axioms'] = get_number_axioms(brain_as_graph)
    df.loc[idx, 'Total aBox axioms'] = get_number_aBox_axioms(brain_as_graph)
    df.loc[idx, 'Total tBox axioms'] = get_number_tBox_axioms(brain_as_graph)
    #####
    print(f"\tCalculating brain metrics")
    df.loc[idx, 'Total semantic statements'] = 0
    df.loc[idx, 'Total sources'] = 0
    return df


def copy_metrics(df, idx):
    print(f"\tCopying graph metrics")
    df.loc[idx, 'Total nodes'] = df.loc[idx - 1, 'Total nodes']
    df.loc[idx, 'Total edges'] = df.loc[idx - 1, 'Total edges']
    df.loc[idx, 'Average degree'] = df.loc[idx - 1, 'Average degree']
    df.loc[idx, 'Average degree centrality'] = df.loc[idx - 1, 'Average degree centrality']
    df.loc[idx, 'Average closeness'] = df.loc[idx - 1, 'Average closeness']
    # df.loc[idx, 'Average betweenness'] = df.loc[idx-1, 'Average betweenness']
    df.loc[idx, 'Average degree connectivity'] = df.loc[idx - 1, 'Average degree connectivity']
    df.loc[idx, 'Average assortativity'] = df.loc[idx - 1, 'Average assortativity']
    df.loc[idx, 'Average node connectivity'] = df.loc[idx - 1, 'Average node connectivity']
    df.loc[idx, 'Number of components'] = df.loc[idx - 1, 'Number of components']
    df.loc[idx, 'Number of strong components'] = df.loc[idx - 1, 'Number of strong components']
    # df.loc[idx, 'Shortest path'] = df.loc[idx-1, 'Shortest path']
    df.loc[idx, 'Centrality entropy'] = df.loc[idx - 1, 'Centrality entropy']
    df.loc[idx, 'Closeness entropy'] = df.loc[idx - 1, 'Closeness entropy']
    df.loc[idx, 'Sparseness'] = df.loc[idx - 1, 'Sparseness']
    df.loc[idx, 'Total explicit triples'] = df.loc[idx - 1, 'Total explicit triples']
    df.loc[idx, 'Total classes'] = df.loc[idx - 1, 'Total classes']
    df.loc[idx, 'Total properties'] = df.loc[idx - 1, 'Total properties']
    df.loc[idx, 'Total instances'] = df.loc[idx - 1, 'Total instances']
    df.loc[idx, 'Total object properties'] = df.loc[idx - 1, 'Total object properties']
    df.loc[idx, 'Total data properties'] = df.loc[idx - 1, 'Total data properties']
    df.loc[idx, 'Total equivalent class properties'] = df.loc[idx - 1, 'Total equivalent class properties']
    df.loc[idx, 'Total subclass properties'] = df.loc[idx - 1, 'Total subclass properties']
    df.loc[idx, 'Total entities'] = df.loc[idx - 1, 'Total entities']
    df.loc[idx, 'Total inverse entities'] = df.loc[idx - 1, 'Total inverse entities']
    df.loc[idx, 'Ratio of inverse relations'] = df.loc[idx - 1, 'Ratio of inverse relations']
    df.loc[idx, 'Property class ratio'] = df.loc[idx - 1, 'Property class ratio']
    df.loc[idx, 'Average population'] = df.loc[idx - 1, 'Average population']
    df.loc[idx, 'Class property ratio'] = df.loc[idx - 1, 'Class property ratio']
    df.loc[idx, 'Attribute richness'] = df.loc[idx - 1, 'Attribute richness']
    df.loc[idx, 'Inheritance richness'] = df.loc[idx - 1, 'Inheritance richness']
    df.loc[idx, 'Relationship richness'] = df.loc[idx - 1, 'Relationship richness']
    df.loc[idx, 'Object properties ratio'] = df.loc[idx - 1, 'Object properties ratio']
    df.loc[idx, 'Datatype properties ratio'] = df.loc[idx - 1, 'Datatype properties ratio']
    df.loc[idx, 'Total concept assertions'] = df.loc[idx - 1, 'Total concept assertions']
    df.loc[idx, 'Total role assertions'] = df.loc[idx - 1, 'Total role assertions']
    df.loc[idx, 'Total general concept inclusions'] = df.loc[idx - 1, 'Total general concept inclusions']
    df.loc[idx, 'Total domain axioms'] = df.loc[idx - 1, 'Total domain axioms']
    df.loc[idx, 'Total range axioms'] = df.loc[idx - 1, 'Total range axioms']
    df.loc[idx, 'Total role inclusions'] = df.loc[idx - 1, 'Total role inclusions']
    df.loc[idx, 'Total axioms'] = df.loc[idx - 1, 'Total axioms']
    df.loc[idx, 'Total aBox axioms'] = df.loc[idx - 1, 'Total aBox axioms']
    df.loc[idx, 'Total tBox axioms'] = df.loc[idx - 1, 'Total tBox axioms']
    df.loc[idx, 'Total semantic statements'] = df.loc[idx - 1, 'Total semantic statements']
    df.loc[idx, 'Total sources'] = df.loc[idx - 1, 'Total sources']

    return df


def evaluate_conversation():
    # Read list of human evaluations (3 in this case)
    datapath = Path(INPUT_FOLDER)
    dfs = []
    for path in datapath.glob('*.csv'):
        # Read and keep desired data
        temp_df = pd.read_csv(path)
        temp_df = temp_df[['Turn',
                           'System llh', 'MLM llh', 'USR DLcontext', 'USR DLfact', 'Overall Human Rating',
                           'Interesting', 'Engaging', 'Specific', 'Relevant',
                           'Correct', 'Semantically Appropriate', 'Understandable', 'Fluent']]
        dfs.append(temp_df)

    # Average annotations, per turn
    avg_df = pd.concat(dfs).groupby(level=0).mean()

    # Read separate file with rdf_file column
    rdf_df = pd.read_json(SCENARIO_FOLDER + f'turn_to_trig_file.json')

    # Recreate conversation and score graph
    rdf_count = 0
    for idx, row in rdf_df.iterrows():
        print(f"Processing turn {row['Turn']}")

        # if row has a file to rdf, process it and calculate metrics
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
            # bob = URIRef("http://example.org/people/Bob")
            # brain_as_graph.add((bob, RDF.type, FOAF.Person))
            # brain_as_graph.add((bob, RDF.type, bob))
            brain.parse(RDF_FOLDER + row['rdf_file'], format='trig')
            brain_as_graph.parse(RDF_FOLDER + row['rdf_file'], format='trig')
            brain_as_netx = rdflib_to_networkx_multidigraph(brain_as_graph)

            # Calculate metrics (only when needed! otherwise copy row)
            rdf_df = calculate_metrics(brain, brain_as_graph, brain_as_netx, rdf_df, idx)

        # copy over values from last row to avoid recomputing on an unchanged graph
        else:
            rdf_df = copy_metrics(rdf_df, idx)

    full_df = avg_df.merge(rdf_df, left_on='Turn', right_on='Turn')
    save('g1s1', full_df)

    return avg_df


if __name__ == "__main__":
    _ = evaluate_conversation()

    print('ALL DONE')
