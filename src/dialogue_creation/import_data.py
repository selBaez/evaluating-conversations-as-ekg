# encoding: utf-8
import json
import os
import pathlib
import random
import sys
import traceback
from datetime import datetime
from random import choice, getrandbits

import pandas as pd
import requests
from cltl.brain.long_term_memory import LongTermMemory
from cltl.brain.utils.helper_functions import brain_response_to_json
from cltl.entity_linking.linkers import NamedEntityLinker, PronounLinker
from cltl.reply_generation.data.sentences import ELOQUENCE
from cltl.reply_generation.lenka_replier import LenkaReplier
from cltl.triple_extraction.api import Chat
from cltl.triple_extraction.cfg_analyzer import CFGAnalyzer
from cltl.triple_extraction.oie_analyzer import OIEAnalyzer
from cltl.triple_extraction.utils.helper_functions import utterance_to_capsules

# Data
PATH_READ = '/Users/selbaez/Documents/PhD/sandbox/data/MELD characters/MELD-{}.csv'
BRAIN = "http://localhost:7200/repositories/friends"
BRAIN_OIE = "http://localhost:7200/repositories/friends_oie"

ABSOLUTE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = ABSOLUTE_PATH + f'/../../data/e3-friends_oie/scenario1/'
SCENARIO_FOLDER = DATA_FOLDER + f'2022-05-02-13_52_54/'
RDF_FOLDER = SCENARIO_FOLDER + f'rdf/'

# Do better about locations
PLACE_ID = getrandbits(8)
LOCATION = requests.get("https://ipinfo.io").json()

# Time
AIRINGS = pd.read_csv('/Users/selbaez/Documents/PhD/sandbox/data/friends_airings.csv', sep=';')


def select_characters():
    # Add info about characters
    main_characters = ['Chandler', 'Joey', 'Monica', 'Phoebe', 'Rachel', 'Ross']
    sel_character = random.choice(main_characters)
    print(f"------------- WHAT IF LEOLANI WAS {sel_character} IN 'FRIENDS'? -------------")

    return 'Chandler', 'Monica'


def read_data(data_path, character2):
    # Read data
    df = pd.read_csv(data_path, sep='\t').sort_values(by=['Season', 'Episode', 'Dialogue_ID', 'Utterance_ID'])

    # Filter only dialogues with character2
    temp_df = df[['Dialogue_ID', 'Speaker']].groupby('Dialogue_ID', sort=False).agg(lambda x: ','.join(x.unique()))
    dialogue_ids = list(temp_df[temp_df['Speaker'].isin(['Chandler,Monica', 'Monica,Chandler'])].index)
    df = df[df['Dialogue_ID'].isin(dialogue_ids)]

    print(f"WILL PROCESS {len(df)} UTTERANCES\n\n")

    return df


def calculate_airtime(season_episode):
    air_time = AIRINGS[AIRINGS['Season_ep.'] == season_episode]['Original_Air_Date'].values[0]
    air_time = datetime.strptime(air_time, '%d %b %y')

    return air_time


def new_chat(capsule, last_chat):
    # check last id and this id
    if not last_chat or last_chat.id != capsule['Dialogue_ID']:
        # Create chat
        print("\n\n\n----------\t[{}]\tNEW CHAT: \t{}----------\n\n".format(capsule['Dialogue_ID'], capsule['Speaker']))
        next_chat = Chat(capsule['Speaker'])
        next_chat.id = capsule['Dialogue_ID']

    else:
        next_chat = last_chat

    return next_chat


def new_utterance(caps, chat, alternative_capsule=None):
    chat.add_utterance(caps['Utterance'])
    # chat.last_utterance.set_turn(caps['Utterance_ID'])

    if alternative_capsule:
        print(f"CREATED REPLY: \n\t{caps['Speaker']}: {caps['Utterance']}\n")
        print(f"ORIGINAL REPLY: \n\t{alternative_capsule['Speaker']}: {alternative_capsule['Utterance']}\n\n")

    else:
        print(f"UTTERANCE: \n\t{caps['Speaker']}: {caps['Utterance']}\n\n")
    return chat


def link_capsule(linkers, capsule):
    for linker in linkers:
        updated_capsule = linker.link(capsule)
        if updated_capsule:
            return updated_capsule


def prepare_capsule_for_brain(capsule, e_capsule):
    capsule_extras = {
        "context_id": str(capsule['Season']).zfill(4) + str(capsule['Episode']).zfill(4),
        "date": calculate_airtime(str(capsule['Season']) + '-' + str(capsule['Episode'])),
        "place": LOCATION['city'],
        "place_id": PLACE_ID,
        "country": LOCATION['country'],
        "region": LOCATION['region'],
        "city": LOCATION['city'],
        "objects": [],
        "people": []
    }

    e_capsule.update(capsule_extras)

    return e_capsule


def leolani_reply(capsule, extracted_capsules, brain, replier):
    replies = []
    rdf_files = []
    for e_capsule in extracted_capsules:
        # Prepare capsule
        e_capsule = prepare_capsule_for_brain(capsule, e_capsule)

        # Prepare response according to type of utterance
        if e_capsule['utterance_type'].name == "QUESTION":
            brain_response = brain.query_brain(e_capsule)
            response_json = brain_response_to_json(brain_response)
            reply = replier.reply_to_question(response_json)
            replies.append(reply)

        elif e_capsule['utterance_type'].name == "STATEMENT":
            brain_response = brain.update(e_capsule, reason_types=True, create_label=True)
            response_json = brain_response_to_json(brain_response)
            reply = replier.reply_to_statement(response_json, entity_only=False, proactive=True, persist=True)
            replies.append(reply)
            rdf_files.append(brain_response['rdf_log_path'].stem + '.trig')

    if replies:
        return replies, rdf_files
    else:
        return [choice(ELOQUENCE)], rdf_files


def my_turn(capsule, chat, extracted_capsules, brain, replier):
    # Generate reply
    my_reply, rdf_files = leolani_reply(capsule, extracted_capsules, brain, replier)

    # Save utterance
    new_capsule = capsule.copy()
    new_capsule['Speaker'] = 'Leolani'
    new_capsule['Utterance'] = ' '.join(my_reply)
    chat = new_utterance(new_capsule, chat, alternative_capsule=capsule)

    return chat, rdf_files


def others_turn(capsule, chat, analyzer, linkers):
    # New utterance in chat
    chat = new_utterance(capsule, chat)

    # Try to create triple/graph
    capsules = []
    try:
        analyzer.analyze(chat.last_utterance)
        capsules = utterance_to_capsules(chat.last_utterance)

        if capsules:
            # Use linkers to add uris to mentions
            capsules = [link_capsule(linkers, cpsl) for cpsl in capsules]

    except Exception as e:
        print(traceback.format_exc())
        print("I FOUND AN ERROR! {}\n\t\t\t{}".format(e, sys.exc_info()[0]))

    return chat, capsules


def import_dataset(method='lenka'):
    # select character and filter by those with her
    character1, character2 = select_characters()

    # Read data
    df = read_data(data_path=PATH_READ.format(character1), character2=character2)
    # df = df[:10]

    # Create brain connection
    brain_address = BRAIN if method.lower() == 'lenka' else BRAIN_OIE
    brain = LongTermMemory(address=brain_address, log_dir=pathlib.Path(RDF_FOLDER), clear_all=True)

    # Create couple analyzers, a linker, and a replier
    analyzer = CFGAnalyzer() if method.lower() == 'lenka' else OIEAnalyzer()
    linkers = [PronounLinker(brain_address, pathlib.Path(RDF_FOLDER)),
               NamedEntityLinker(brain_address, pathlib.Path(RDF_FOLDER))]
    replier = LenkaReplier()

    # Keep rack of the chat
    chat = None
    utterances = []
    extracted_capsules = []

    for idx, capsule in df.iterrows():
        capsule = capsule.to_dict()

        # Create chat (maybe keep last one)
        chat = new_chat(capsule, chat)

        if capsule['Speaker'] == character1:
            # Parse what "I" said
            chat, rdf_files = my_turn(capsule, chat, extracted_capsules, brain, replier)
            extracted_capsules = []

        elif capsule['Speaker'] == character2:
            # parse what the other person says
            chat, extracted_capsules = others_turn(capsule, chat, analyzer, linkers)
            rdf_files = []

        else:
            continue

        # Produce json
        utterance = {"Turn": len(utterances), "Speaker": capsule['Speaker'], "Response": capsule['Utterance'],
                     "rdf_file": rdf_files}
        utterances.append(utterance)

    with open(SCENARIO_FOLDER + '/turn_to_trig_file.json', 'w') as f:
        js = json.dumps(utterances)
        f.write(js)


if __name__ == "__main__":
    import_dataset(method='oie')
