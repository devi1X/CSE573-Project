from pymetamap import MetaMap
import pandas as pd
import os
from time import sleep


def main():
    # set up header and result csv file
    symptom_header = ['score', 'preferred_name', 'cui']
    result_header = ['content_index', 'score', 'preferred_name', 'cui']
    filename_prefix = "split_file"
    result_prefix = "result"

    # Setup UMLS Server
    metamap_base_dir = '/home/explosionist/metamap_full/public_mm'
    metamap_bin_dir = '/bin/metamap20'
    metamap_pos_server_dir = '/bin/skrmedpostctl'
    metamap_wsd_server_dir = '/bin/wsdserverctl'

    # Start servers
    os.system(metamap_base_dir + metamap_pos_server_dir + ' start')  # Part of speech tagger
    os.system(metamap_base_dir + metamap_wsd_server_dir + ' start')  # Word sense disambiguation

    # Sleep a bit to give time for these servers to start up
    sleep(40)

    # get connect with metamap server
    metam = MetaMap.get_instance(metamap_base_dir + metamap_bin_dir)


    # todo: change
    for i in range(5):
        data = pd.read_csv(f"{filename_prefix}{i+1}.csv")
        result = pd.DataFrame(columns=result_header)
        data_list = data.values.tolist()
        sents = [[row[0], row[-1]] for row in data_list]

        # sentence contain two elements:
        # sentence[0]: content index
        # sentence[1]: content
        for sentence in sents:
            # get rephrased concepts and errors
            concepts, error = metam.extract_concepts([sentence[1],],
                                                     word_sense_disambiguation=True,
                                                     ignore_stop_phrases=True)
            content = [get_symptom(concept, symptom_header) for concept in concepts]

            high_score_concepts = pd.DataFrame(content, columns=symptom_header)
            high_score_concepts.insert(0, 'content_index', sentence[0])
            result = pd.concat([result, high_score_concepts])

        # todo: change
        result.to_csv(f"{result_prefix}{i+1}.csv", index=False)


# define a method to extract symptom name and id
def get_symptom(concept, key_list):
    con_dict = concept._asdict()
    con_list = [con_dict.get(key) for key in key_list]
    return (tuple(con_list))


if __name__ == '__main__':
    # run the main program
    main()
