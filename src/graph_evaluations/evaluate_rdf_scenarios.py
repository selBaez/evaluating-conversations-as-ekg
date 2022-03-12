import os
from pathlib import Path

import pandas as pd
from rdflib import ConjunctiveGraph
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
from tqdm import tqdm

from src.graph_evaluations.metrics.brain_measures import *
from src.graph_evaluations.metrics.graph_measures import *
from src.graph_evaluations.metrics.ontology_measures import *

ABSOLUTE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = ABSOLUTE_PATH + f'/../../data/g2-jaap/scenario1/'
SCENARIO_FOLDER = DATA_FOLDER + f'2021-12-10-10_29_17/'
RDF_FOLDER = SCENARIO_FOLDER + f'rdf/2021-12-10-10-29/'
SCENARIO_ID = 'g2s1'
INPUT_FOLDER = DATA_FOLDER + f'human_evaluations/'
OUTPUT_FOLDER = DATA_FOLDER + f'automatic_evaluations/'


def save(file_num, df):
    df = df.drop(columns=['Speaker', 'Response', 'rdf_file'])
    df.to_csv(OUTPUT_FOLDER + f'{file_num}.csv', index=False)


def calculate_metrics(brain_as_graph, brain_as_netx, df, idx):
    print(f"\tCalculating graph metrics")
    df.loc[idx, 'GROUP A - Total nodes'] = get_count_nodes(brain_as_netx)
    df.loc[idx, 'GROUP A - Total edges'] = get_count_edges(brain_as_netx)
    df.loc[idx, 'GROUP A - Average degree'] = get_avg_degree(brain_as_netx)
    df.loc[idx, 'GROUP A - Average degree centrality'] = get_avg_degree_centr(brain_as_netx)
    df.loc[idx, 'GROUP A - Average closeness'] = get_avg_closeness(brain_as_netx)
    # df.loc[idx, 'GROUP A - Average betweenness'] = get_avg_betweenness(brain_as_netx)
    df.loc[idx, 'GROUP A - Average degree connectivity'] = get_degree_connectivity(brain_as_netx)
    df.loc[idx, 'GROUP A - Average assortativity'] = get_assortativity(brain_as_netx)  # good
    df.loc[idx, 'GROUP A - Average node connectivity'] = get_node_connectivity(brain_as_netx)
    df.loc[idx, 'GROUP A - Number of components'] = get_number_components(brain_as_netx)
    df.loc[idx, 'GROUP A - Number of strong components'] = get_assortativity(brain_as_netx)
    # df.loc[idx, 'GROUP A - Shortest path'] = get_shortest_path(brain_as_netx)
    df.loc[idx, 'GROUP A - Centrality entropy'] = get_entropy_centr(brain_as_netx)
    df.loc[idx, 'GROUP A - Closeness entropy'] = get_entropy_clos(brain_as_netx)
    df.loc[idx, 'GROUP A - Sparseness'] = get_sparseness(brain_as_netx)  # good
    ####
    print(f"\tCalculating RDF graph metrics")
    df.loc[idx, 'GROUP B - Total classes'] = get_number_classes(brain_as_graph)
    df.loc[idx, 'GROUP B - Total properties'] = get_number_properties(brain_as_graph)
    # df.loc[idx, 'GROUP B - Total instances']  = get_number_instances(brain_as_graph)
    # df.loc[idx, 'GROUP B - Total object properties']  = get_number_properties_object(brain_as_graph)
    # df.loc[idx, 'GROUP B - Total data properties']  = get_number_properties_datatype(brain_as_graph)
    # df.loc[idx, 'GROUP B - Total equivalent class properties']  = get_number_properties_equivClass(brain_as_graph)
    # df.loc[idx, 'GROUP B - Total subclass properties']  = get_number_properties_subclass(brain_as_graph)
    # df.loc[idx, 'GROUP B - Total entities']  = get_number_entities(brain_as_graph)
    # df.loc[idx, 'GROUP B - Total inverse entities']  = get_number_inverse(brain_as_graph)
    # df.loc[idx, 'GROUP B - Ratio of inverse relations']  = get_ratio_inverse_relations(brain_as_graph)
    # df.loc[idx, 'GROUP B - Property class ratio']  = get_property_class_ratio(brain_as_graph)
    df.loc[idx, 'GROUP B - Average population'] = get_avg_population(brain_as_graph)
    # df.loc[idx, 'GROUP B - Class property ratio']  = get_class_property_ratio(brain_as_graph)
    df.loc[idx, 'GROUP B - Attribute richness'] = get_attribute_richness(brain_as_graph)
    # df.loc[idx, 'GROUP B - Inheritance richness']  = get_inheritance_richness(brain_as_graph)
    df.loc[idx, 'GROUP B - Relationship richness'] = get_relationship_richness(brain_as_graph)
    # df.loc[idx, 'GROUP B - Object properties ratio']  = get_ratio_object_properties(brain_as_graph)
    # df.loc[idx, 'GROUP B - Datatype properties ratio']  = get_ratio_datatype_properties(brain_as_graph)
    # df.loc[idx, 'GROUP B - Total concept assertions']  = get_number_concept_assertions(brain_as_graph)
    # df.loc[idx, 'GROUP B - Total role assertions']  = get_number_role_assertions(brain_as_graph)
    # df.loc[idx, 'GROUP B - Total general concept inclusions']  = get_number_GCI(brain_as_graph)
    # df.loc[idx, 'GROUP B - Total domain axioms']  = get_number_domain_axioms(brain_as_graph)
    # df.loc[idx, 'GROUP B - Total range axioms']  = get_number_range_axioms(brain_as_graph)
    # df.loc[idx, 'GROUP B - Total role inclusions']  = get_number_role_inclusion(brain_as_graph)
    df.loc[idx, 'GROUP B - Total axioms'] = get_number_axioms(brain_as_graph)
    # df.loc[idx, 'GROUP B - Total aBox axioms']  = get_number_aBox_axioms(brain_as_graph)
    # df.loc[idx, 'GROUP B - Total tBox axioms']  = get_number_tBox_axioms(brain_as_graph)
    #####
    print(f"\tCalculating brain metrics")
    df.loc[idx, 'GROUP C - Total triples'] = get_number_triples(brain_as_graph)  # good
    df.loc[idx, 'GROUP C - Total world instances'] = get_number_grasp_instances(brain_as_graph)
    df.loc[idx, 'GROUP C - Total claims'] = get_number_statements(brain_as_graph)
    df.loc[idx, 'GROUP C - Total perspectives'] = get_number_perspectives(brain_as_graph)
    df.loc[idx, 'GROUP C - Total mentions'] = get_number_mentions(brain_as_graph)
    df.loc[idx, 'GROUP C - Total conflicts'] = get_number_negation_conflicts(brain_as_graph)
    df.loc[idx, 'GROUP C - Total sources'] = get_number_sources(brain_as_graph)
    df.loc[idx, 'GROUP C - Total interactions'] = get_number_chats(brain_as_graph)
    df.loc[idx, 'GROUP C - Total utterances'] = get_number_utterances(brain_as_graph)

    df.loc[idx, 'GROUP C - Ratio claim to triples'] = df.loc[idx, 'GROUP C - Total claims'] / df.loc[
        idx, 'GROUP C - Total triples']  # how much knowledge
    df.loc[idx, 'GROUP C - Ratio perspectives to triples'] = df.loc[idx, 'GROUP C - Total perspectives'] / df.loc[
        idx, 'GROUP C - Total triples']  # how much diversity of opinion
    df.loc[idx, 'GROUP C - Ratio conflicts to triples'] = df.loc[idx, 'GROUP C - Total conflicts'] / df.loc[
        idx, 'GROUP C - Total triples']  # how much conflicting info
    df.loc[idx, 'GROUP C - Ratio perspectives to claims'] = df.loc[idx, 'GROUP C - Total perspectives'] / df.loc[
        idx, 'GROUP C - Total claims'] if df.loc[idx, 'GROUP C - Total claims'] != 0 else 0  # density of opinions
    df.loc[idx, 'GROUP C - Ratio mentions to claims'] = df.loc[idx, 'GROUP C - Total mentions'] / df.loc[
        idx, 'GROUP C - Total claims'] if df.loc[idx, 'GROUP C - Total claims'] != 0 else 0  # density of mentions
    df.loc[idx, 'GROUP C - Ratio conflicts to claims'] = df.loc[idx, 'GROUP C - Total conflicts'] / df.loc[
        idx, 'GROUP C - Total claims'] if df.loc[idx, 'GROUP C - Total claims'] != 0 else 0  # density of conflicts

    df.loc[idx, 'GROUP C - Average perspectives per claim'] = get_average_views_per_factoid(brain_as_graph)
    df.loc[idx, 'GROUP C - Average mentions per claim'] = get_average_mentions_per_factoid(brain_as_graph)
    df.loc[idx, 'GROUP C - Average turns per interaction'] = get_average_turns_per_interaction(brain_as_graph)
    df.loc[idx, 'GROUP C - Average claims per source'] = get_average_factoids_per_source(brain_as_graph)
    df.loc[idx, 'GROUP C - Average perspectives per source'] = get_average_views_per_source(brain_as_graph)
    return df


def copy_metrics(df, idx):
    print(f"\tCopying graph metrics")
    df.loc[idx, 'GROUP A - Total nodes'] = df.loc[idx - 1, 'GROUP A - Total nodes']
    df.loc[idx, 'GROUP A - Total edges'] = df.loc[idx - 1, 'GROUP A - Total edges']
    df.loc[idx, 'GROUP A - Average degree'] = df.loc[idx - 1, 'GROUP A - Average degree']
    df.loc[idx, 'GROUP A - Average degree centrality'] = df.loc[idx - 1, 'GROUP A - Average degree centrality']
    df.loc[idx, 'GROUP A - Average closeness'] = df.loc[idx - 1, 'GROUP A - Average closeness']
    # df.loc[idx, 'GROUP A - Average betweenness'] = df.loc[idx-1, 'GROUP A - Average betweenness'] 
    df.loc[idx, 'GROUP A - Average degree connectivity'] = df.loc[idx - 1, 'GROUP A - Average degree connectivity']
    df.loc[idx, 'GROUP A - Average assortativity'] = df.loc[idx - 1, 'GROUP A - Average assortativity']
    df.loc[idx, 'GROUP A - Average node connectivity'] = df.loc[idx - 1, 'GROUP A - Average node connectivity']
    df.loc[idx, 'GROUP A - Number of components'] = df.loc[idx - 1, 'GROUP A - Number of components']
    df.loc[idx, 'GROUP A - Number of strong components'] = df.loc[idx - 1, 'GROUP A - Number of strong components']
    # df.loc[idx, 'GROUP A - Shortest path'] = df.loc[idx-1, 'GROUP A - Shortest path'] 
    df.loc[idx, 'GROUP A - Centrality entropy'] = df.loc[idx - 1, 'GROUP A - Centrality entropy']
    df.loc[idx, 'GROUP A - Closeness entropy'] = df.loc[idx - 1, 'GROUP A - Closeness entropy']
    df.loc[idx, 'GROUP A - Sparseness'] = df.loc[idx - 1, 'GROUP A - Sparseness']

    df.loc[idx, 'GROUP B - Total classes'] = df.loc[idx - 1, 'GROUP B - Total classes']
    df.loc[idx, 'GROUP B - Total properties'] = df.loc[idx - 1, 'GROUP B - Total properties']
    # df.loc[idx, 'GROUP B - Total instances']  = df.loc[idx - 1, 'GROUP B - Total instances'] 
    # df.loc[idx, 'GROUP B - Total object properties']  = df.loc[idx - 1, 'GROUP B - Total object properties'] 
    # df.loc[idx, 'GROUP B - Total data properties']  = df.loc[idx - 1, 'GROUP B - Total data properties'] 
    # df.loc[idx, 'GROUP B - Total equivalent class properties']  = df.loc[idx - 1, 'GROUP B - Total equivalent class properties'] 
    # df.loc[idx, 'GROUP B - Total subclass properties']  = df.loc[idx - 1, 'GROUP B - Total subclass properties'] 
    # df.loc[idx, 'GROUP B - Total entities']  = df.loc[idx - 1, 'GROUP B - Total entities'] 
    # df.loc[idx, 'GROUP B - Total inverse entities']  = df.loc[idx - 1, 'GROUP B - Total inverse entities'] 
    # df.loc[idx, 'GROUP B - Ratio of inverse relations']  = df.loc[idx - 1, 'GROUP B - Ratio of inverse relations'] 
    # df.loc[idx, 'GROUP B - Property class ratio']  = df.loc[idx - 1, 'GROUP B - Property class ratio'] 
    df.loc[idx, 'GROUP B - Average population'] = df.loc[idx - 1, 'GROUP B - Average population']
    # df.loc[idx, 'GROUP B - Class property ratio']  = df.loc[idx - 1, 'GROUP B - Class property ratio'] 
    df.loc[idx, 'GROUP B - Attribute richness'] = df.loc[idx - 1, 'GROUP B - Attribute richness']
    # df.loc[idx, 'GROUP B - Inheritance richness']  = df.loc[idx - 1, 'GROUP B - Inheritance richness'] 
    df.loc[idx, 'GROUP B - Relationship richness'] = df.loc[idx - 1, 'GROUP B - Relationship richness']
    # df.loc[idx, 'GROUP B - Object properties ratio']  = df.loc[idx - 1, 'GROUP B - Object properties ratio'] 
    # df.loc[idx, 'GROUP B - Datatype properties ratio']  = df.loc[idx - 1, 'GROUP B - Datatype properties ratio'] 
    # df.loc[idx, 'GROUP B - Total concept assertions']  = df.loc[idx - 1, 'GROUP B - Total concept assertions'] 
    # df.loc[idx, 'GROUP B - Total role assertions']  = df.loc[idx - 1, 'GROUP B - Total role assertions'] 
    # df.loc[idx, 'GROUP B - Total general concept inclusions']  = df.loc[idx - 1, 'GROUP B - Total general concept inclusions'] 
    # df.loc[idx, 'GROUP B - Total domain axioms']  = df.loc[idx - 1, 'GROUP B - Total domain axioms'] 
    # df.loc[idx, 'GROUP B - Total range axioms']  = df.loc[idx - 1, 'GROUP B - Total range axioms'] 
    # df.loc[idx, 'GROUP B - Total role inclusions']  = df.loc[idx - 1, 'GROUP B - Total role inclusions'] 
    df.loc[idx, 'GROUP B - Total axioms'] = df.loc[idx - 1, 'GROUP B - Total axioms']
    # df.loc[idx, 'GROUP B - Total aBox axioms']  = df.loc[idx - 1, 'GROUP B - Total aBox axioms'] 
    # df.loc[idx, 'GROUP B - Total tBox axioms']  = df.loc[idx - 1, 'GROUP B - Total tBox axioms'] 

    df.loc[idx, 'GROUP C - Total triples'] = df.loc[idx - 1, 'GROUP C - Total triples']
    df.loc[idx, 'GROUP C - Total world instances'] = df.loc[idx - 1, 'GROUP C - Total world instances']
    df.loc[idx, 'GROUP C - Total claims'] = df.loc[idx - 1, 'GROUP C - Total claims']
    df.loc[idx, 'GROUP C - Total perspectives'] = df.loc[idx - 1, 'GROUP C - Total perspectives']
    df.loc[idx, 'GROUP C - Total mentions'] = df.loc[idx - 1, 'GROUP C - Total mentions']
    df.loc[idx, 'GROUP C - Total conflicts'] = df.loc[idx - 1, 'GROUP C - Total conflicts']
    df.loc[idx, 'GROUP C - Total sources'] = df.loc[idx - 1, 'GROUP C - Total sources']
    df.loc[idx, 'GROUP C - Total interactions'] = df.loc[idx, 'GROUP C - Total interactions']
    df.loc[idx, 'GROUP C - Total utterances'] = df.loc[idx - 1, 'GROUP C - Total utterances']

    df.loc[idx, 'GROUP C - Ratio claim to triples'] = df.loc[idx - 1, 'GROUP C - Ratio claim to triples']
    df.loc[idx, 'GROUP C - Ratio perspectives to triples'] = df.loc[idx - 1, 'GROUP C - Ratio perspectives to triples']
    df.loc[idx, 'GROUP C - Ratio conflicts to triples'] = df.loc[idx - 1, 'GROUP C - Ratio conflicts to triples']
    df.loc[idx, 'GROUP C - Ratio perspectives to claims'] = df.loc[idx - 1, 'GROUP C - Ratio perspectives to claims']
    df.loc[idx, 'GROUP C - Ratio mentions to claims'] = df.loc[idx - 1, 'GROUP C - Ratio mentions to claims']
    df.loc[idx, 'GROUP C - Ratio conflicts to claims'] = df.loc[idx - 1, 'GROUP C - Ratio conflicts to claims']

    df.loc[idx, 'GROUP C - Average perspectives per claim'] = df.loc[
        idx - 1, 'GROUP C - Average perspectives per claim']
    df.loc[idx, 'GROUP C - Average mentions per claim'] = df.loc[idx - 1, 'GROUP C - Average mentions per claim']
    df.loc[idx, 'GROUP C - Average turns per interaction'] = df.loc[idx - 1, 'GROUP C - Average turns per interaction']
    df.loc[idx, 'GROUP C - Average claims per source'] = df.loc[idx - 1, 'GROUP C - Average claims per source']
    df.loc[idx, 'GROUP C - Average perspectives per source'] = df.loc[
        idx - 1, 'GROUP C - Average perspectives per source']

    return df


def evaluate_conversation():
    # Read list of human evaluations
    datapath = Path(INPUT_FOLDER)
    dfs = []
    for path in datapath.glob('*.csv'):
        print(f"Found csv {path}")
        # Read and keep desired data
        try:
            temp_df = pd.read_csv(path)
        except:
            try:
                temp_df = pd.read_csv(path, sep=';')
            except:
                print(f"Could not load {path}")
                continue

        temp_df = temp_df[['Turn',
                           'System llh', 'MLM llh', 'USR DLcontext', 'USR DLfact',
                           'Overall Human Rating',
                           'Interesting', 'Engaging', 'Specific', 'Relevant',
                           'Correct', 'Semantically Appropriate', 'Understandable', 'Fluent']]
        dfs.append(temp_df)

    # Average annotations, per turn
    avg_df = pd.concat(dfs).groupby(level=0).mean()

    # Read separate file with rdf_file column
    rdf_df = pd.read_json(SCENARIO_FOLDER + f'turn_to_trig_file.json')

    # Merge
    full_df = avg_df.merge(rdf_df, left_on='Turn', right_on='Turn')

    # Recreate conversation and score graph
    rdf_count = 0
    for idx, row in tqdm(full_df.iterrows()):
        print(f"Processing turn {row['Turn']}")

        # if row has a file to rdf, process it and calculate metrics
        if type(row['rdf_file']) == str:
            # Update count
            rdf_count += 1
            print(f"\tFound RDF, cumulative: {rdf_count}")

            # clear brain (for computational purposes)
            print(f"\tClear brain")
            brain_as_graph = ConjunctiveGraph()

            # Add new
            print(f"\tAdding triples to brains")
            brain_as_graph.parse(RDF_FOLDER + row['rdf_file'], format='trig')
            brain_as_netx = rdflib_to_networkx_multidigraph(brain_as_graph)

            # Calculate metrics (only when needed! otherwise copy row)
            full_df = calculate_metrics(brain_as_graph, brain_as_netx, full_df, idx)

        # copy over values from last row to avoid recomputing on an unchanged graph
        else:
            full_df = copy_metrics(full_df, idx)

        # Copy human ratings for ease of plotting
        for human_metric in ['Overall Human Rating', 'Interesting', 'Engaging', 'Specific', 'Relevant',
                             'Correct', 'Semantically Appropriate', 'Understandable', 'Fluent']:
            if np.isnan(row[human_metric]) and idx != 0:
                full_df.loc[idx, human_metric] = full_df.loc[idx - 1, human_metric]

    save(SCENARIO_ID, full_df)

    return avg_df


if __name__ == "__main__":
    _ = evaluate_conversation()

    print('ALL DONE')
