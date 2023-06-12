import pandas as pd
import warnings
import re

def conversion_csv_to_json(csv_file):
    """
    Test conversion function
    """
    df = pd.read_csv(csv_file, na_filter=False, dtype='str')
    elab_json = {}
    elab_dict = {}
    pos = 1

    list_of_dict = df.to_dict('records')
    for redcap_field_dict in list_of_dict:
        # Skip the logic fields because ElabFTW does not understand them
        if redcap_field_dict['Branching Logic (Show field only if...)'] != '':
            continue
        if redcap_field_dict['Variable / Field Name'] == 'record_id':
            continue
        if redcap_field_dict['Field Type'] == 'text':
            if redcap_field_dict['Text Validation Type OR Show Slider Number'] == 'number' or redcap_field_dict[
                'Text Validation Type OR Show Slider Number'] == 'integer':
                elab_dict = number_to_dict(redcap_field_dict)
            elif redcap_field_dict['Text Validation Type OR Show Slider Number'] == 'date_dmy':
                elab_dict = date_to_dict(redcap_field_dict)
            else:
                elab_dict = text_to_dict(redcap_field_dict)
        elif redcap_field_dict['Field Type'] == 'dropdown':
            elab_dict = dropdown_to_dict(redcap_field_dict)
        elif redcap_field_dict['Field Type'] == 'notes':
            elab_dict = notes_to_dict(redcap_field_dict)
        elif redcap_field_dict['Field Type'] == 'radio':
            elab_dict = radio_to_dict(redcap_field_dict)
        elif redcap_field_dict['Field Type'] == 'checkbox':
            elab_dict = checkbox_to_dict(redcap_field_dict)
        else:
            pass
        elab_json.update(elab_dict)
    final_elab = {
        "extra_fields": elab_json
    }

    for key in final_elab["extra_fields"].keys():
        final_elab["extra_fields"][key].update({"position": pos})
        pos += 1

    return final_elab


def text_to_dict(redcap_field_dict):
    temp_elab_dict = {
        redcap_field_dict['Field Label']: {
            "type": "text",
            "value": "",
            "description": redcap_field_dict['Field Note']},
    }
    return temp_elab_dict


def number_to_dict(redcap_field_dict):
    # text mean multiples types in json. Need to define all of them
    temp_elab_dict = {
        redcap_field_dict['Field Label']: {
            "type": "number",
            "value": "",
            "description": redcap_field_dict['Field Note']},
    }
    return temp_elab_dict


def date_to_dict(redcap_field_dict):
    temp_elab_dict = {
        redcap_field_dict['Field Label']: {
            "type": "date",
            "value": "",
            "description": redcap_field_dict['Field Note']},
    }
    return temp_elab_dict


def radio_to_dict(redcap_field_dict):
    assert redcap_field_dict["Field Type"] == "radio"
    redcap_choice_str = redcap_field_dict["Choices, Calculations, OR Slider Labels"]
    redcap_annotation_str = redcap_field_dict["Field Annotation"]
    choice_labels, default_choice_label = parse_choices(redcap_choice_str, redcap_annotation_str)
    temp_elab_dict = {
        redcap_field_dict['Field Label']: {
            "type": "radio",
            "value": default_choice_label,
            "options": choice_labels,
            "description": redcap_field_dict['Field Note']
        },
    }
    return temp_elab_dict


def checkbox_to_dict(redcap_field_dict):
    assert redcap_field_dict["Field Type"] == "checkbox"
    redcap_choice_str = redcap_field_dict["Choices, Calculations, OR Slider Labels"]
    redcap_annotation_str = redcap_field_dict["Field Annotation"]
    choice_labels, default_choice_label = parse_choices(redcap_choice_str, redcap_annotation_str)
    temp_elab_dict = {
        redcap_field_dict['Field Label']: {
            "type": "select",
            "value": default_choice_label,
            "options": choice_labels,
            "description": redcap_field_dict['Field Note'],
            "allow_multi_values": True
        },
    }

    return temp_elab_dict


def dropdown_to_dict(redcap_field_dict):
    assert redcap_field_dict["Field Type"] == "dropdown"
    redcap_choice_str = redcap_field_dict["Choices, Calculations, OR Slider Labels"]
    redcap_annotation_str = redcap_field_dict["Field Annotation"]
    choice_labels, default_choice_label = parse_choices(redcap_choice_str, redcap_annotation_str)

    # dropdown is always select type in json
    temp_elab_dict = {
        redcap_field_dict['Field Label']: {
            "type": "select",
            "value": default_choice_label,
            "options": choice_labels,
            "description": redcap_field_dict['Field Note']
        },
    }
    return temp_elab_dict


def notes_to_dict(redcap_field_dict):
    temp_elab_dict = {redcap_field_dict['Field Label']: {
        "type": "text",
        "value": "",
        "description": redcap_field_dict['Field Note']},
    }
    return temp_elab_dict


def parse_choices(choice_str, annotation_str):
    """
    Extract choice labels and default choice label from redcap
    "Choices, Calculations, OR Slider Labels" and "Annotations"

    Returns
    -------
    (list, str)
        first entry is the list of default choice labels
        second entry is the default choice labels (is value of first entry)

    """
    # default return values
    choice_labels = []
    default_choice_label = ''

    choice_match = re.findall('(?:\|?)\s?(?P<choice>\w+)\s?,\s?(?P<label>[^,|]+?)\s*(?:\||$)', choice_str)
    if choice_match:
        choice_keys, choice_labels = zip(*choice_match)
        if '@DEFAULT=' in annotation_str:
            choice_selector = '|'.join(choice_keys)
            match = re.match('@DEFAULT=["\'](' + choice_selector + ')["\']', annotation_str)
            if match:
                default_choice_key = match.groups()[0]
                default_choice_label = choice_labels[choice_keys.index(default_choice_key)]
            else:
                warnings.warn(f'Could not determine default choice for {annotation_str}')

    choice_labels = [re.sub(r'\{.*?\}', '', label) for label in choice_labels]
    # Removal of embedded fields used in RedCap ( {...} ) as there is no equivalent in ElabFTW
    default_choice_label = re.sub(r'\{.*?\}', '', default_choice_label)

    return list(choice_labels), default_choice_label
