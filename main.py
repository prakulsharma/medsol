import itertools
import bs4
import requests
from utils import *


def get_interactions_from_med(med_names: str, print_output: bool = False):
    med_names = med_names.split(",")
    med_names = [med_name.strip() for med_name in med_names]

    if len(med_names) == 1:
        return "Enter more than 1 medicine name", None

    drug_list, med_drugs_dict = get_drug_name_from_med(med_names, print_output)
    med_drugs_dict = drug_dict_processing(med_drugs_dict)

    if type(drug_list) == list:
        drug_list_final = final_drug_list(drug_list)
        print('Main.py, Drug List: ', drug_list_final)
        interaction_dict_list = get_interactions_from_drug(drug_list_final, print_output)
        return interaction_dict_list, med_drugs_dict

    print('Main.py, Drug List: ', drug_list)
    return drug_list, None


def get_drug_name_from_med(med_names: str, print_output: bool = False):
    all_drug_names_dict = {}
    for med_name in med_names:
        url = 'https://www.mims.com/india/drug/info/' + med_name
        request_result = requests.get(url)
        soup = bs4.BeautifulSoup(request_result.text, "html.parser")
        try:
            medicine_raw_text = soup.find("div", "monograph-section-content").text
            # Removing white spaces and tabs
            medicine_raw_text = re.sub("[\n\r]", "", medicine_raw_text)
            # Making all text lowercase
            medicine_raw_text = medicine_raw_text.lower()
            # Resolving text issues for cases with ":"
            if ":" in medicine_raw_text:
                drug_list = clean_text(medicine_raw_text)
            else:
                drug_list = clean_text_without_colon(medicine_raw_text)
            all_drug_names_dict[med_name] = drug_list
        except Exception as e:
            print("No drug found for {}".format(med_name))
            all_drug_names_dict[med_name] = ["Not in database"]
    if not bool(all_drug_names_dict):
        return "No drugs found in database"
    for med_name, drug_list in all_drug_names_dict.items():
        clean_drug_list = remove_common_drugs(drug_list)
        all_drug_names_dict[med_name] = clean_drug_list

    if print_output:
        for key, value in all_drug_names_dict.items():
            print("{}    : {}".format(key, value))

    return list(itertools.chain(*list(all_drug_names_dict.values()))), all_drug_names_dict


def get_interactions_from_drug(drug_names: list, print_output: bool = False):
    lst = []
    interaction_dict_list = []
    for drug_name in drug_names:
        if print_output:
            print("trying for {}".format(drug_name))
        url = "https://rxnav.nlm.nih.gov/REST/rxcui.json?name={}&search=1".format(drug_name)
        data = requests.get(url).json()
        try:
            lst.append(data['idGroup']['rxnormId'][0])
        except Exception as e:
            print("Couldn't find data for {}".format(drug_name))

    url = 'https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis='

    for x in lst:
        url = url + x + '+'

    try:
        result = requests.get(url[:-1]).json()
        for fullInteractionTypeGroup in result['fullInteractionTypeGroup']:
            for fullInteractionType in fullInteractionTypeGroup['fullInteractionType']:
                for interactionPair in fullInteractionType['interactionPair']:
                    drug1 = interactionPair['interactionConcept'][0]['sourceConceptItem']['name']
                    drug2 = interactionPair['interactionConcept'][1]['sourceConceptItem']['name']

                    interactions_dict = {
                        'Drug1': drug1,
                        'Drug2': drug2,
                        'Severity': interactionPair['severity'],
                        'Desc': interactionPair['description']
                    }

                    interaction_dict_list.append(interactions_dict)

                    print("Interaction between {} and {}".format(drug1, drug2))
                    print("Severity: {} ".format(interactionPair['severity']))
                    print("Interaction: {}".format(interactionPair['description']))
                    print("-------")
        return interaction_dict_list
    except Exception as e:
        return "No interactions found in database"


if __name__ == "__main__":
    raw_text = "dolo, CCM"
    get_interactions_from_med(raw_text, print_output=True)
