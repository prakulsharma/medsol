import re


def clean_text(text):
    lst = []
    pattern = "[\d\.\s]+(mg[//]?|ml)+"
    clean_string = re.sub(pattern, ' ', text)

    pattern = "\([a-z]+\)"
    clean_string = re.sub(pattern, ' ', clean_string)

    pattern = ":\s*[a-z\,\-\s]+"
    final_string = re.findall(pattern, clean_string)

    for drug in final_string:
        lst.append(drug.split(":")[1])

    return lst


def clean_text_without_colon(text):
    #     pattern = "[\r\n]"
    #     clean_string = re.sub(pattern, '', text )

    pattern = "[a-z,\s]+"
    clean_string = re.findall(pattern, text)

    # Assuming all text in the first string only
    lst = []
    lst.append(clean_string[0])
    return lst


def remove_common_drugs(drugs_list):
    updated_drug_list = []
    for drug in drugs_list:
        drug = drug.strip()

        if len(updated_drug_list) == 0:
            updated_drug_list.append(drug)
        else:
            if drug not in updated_drug_list:
                updated_drug_list.append(drug)
    return updated_drug_list


def correct_dict(drug_dict):
    for key, value in drug_dict.items():
        lst = []
        if len(value) > 1:
            for item in value:
                if ',' in item:
                    if len(item) > 1:
                        for sub_item in item.split(','):
                            lst.append(sub_item)
                        drug_dict[key] = lst
        else:
            for item in value:
                if "," in item:
                    for sub_item in item.split(","):
                        lst.append(sub_item)
                    drug_dict[key] = lst
    return drug_dict


def final_drug_list(drug_list):
    final_drugs = []
    for drug in drug_list:
        names = drug.split(',')
        for name in names:
            final_drugs.append(name.strip())

    return final_drugs


def drug_dict_processing(med_drug_dict):
    for med, druglist in med_drug_dict.items():
        org_list = druglist
        final_drugs = []

        for drug in org_list:
            names = drug.split(',')
            for name in names:
                final_drugs.append(name.strip())

        med_drug_dict[med] = final_drugs
    return med_drug_dict