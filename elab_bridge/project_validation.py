import pathlib
import json

import pandas as pd
import warnings

import elab_bridge


template_dir = pathlib.Path(elab_bridge.__file__).parent / 'template_parts'

def _validate_extra_fields(to_validate, validate_against, validate_values=False):
    """
    Validate one dictionary of extra fields against another

    Parameters
    ----------
    to_validate: dict
        The dictionary of fields to validate
    validate_against: dict
        The dictionary of fields to validate against
    validate_values: bool, list
        Include attribute values in the validation process.
        If True, values are checked for equality. If False, values are ignored.
        In case of a list, only attribute names of that list are compared for equality.
        Default: False

    Raises
    ------
        ValueError in case of unsuccessful validation
    """

    # check no field is missing
    missing_fields = set(validate_against).difference(to_validate)
    if missing_fields:
        raise ValueError(f'Failed validation: Missing field(s) in extra fields: {missing_fields}')

    for field_name, field_content in validate_against.items():

        # checking field attributes
        missing_attributes = set(field_content).difference(to_validate[field_name])
        if missing_attributes:
            raise ValueError(f'Failed validation: Missing attribute(s) in extra field "{field_name}": {missing_attributes}')

        if validate_values:
            for key, value in field_content.items():

                if isinstance(validate_values, list) and key not in validate_values:
                    continue

                # checking non-empty field attribute values
                if value != to_validate[field_name][key]:
                    raise ValueError(
                        f'Template attribute value not preserved in form: {field_name}>{key}:{value}. '
                        f'Instead found {to_validate[field_name][key]}')

def validate_project_against_template_parts(project, *templates):
    """
    Validate a built project json

    Parameters
    ----------
    project: str, buffer
        Filepath of the json file or json buffer of the built project
    templates: str, list
        List of file paths of the template part jsons.

    Returns
    ----------
    bool  
        True if the validation was successful
    """

    with open(project, 'r') as p:
        form = json.load(p)

    assert 'elabftw' in form
    assert 'extra_fields' in form

    if not templates:
        warnings.warn('No template selected list is empty')

    for template_name in templates:
        template_path = (template_dir / template_name).with_suffix('.json')

        if not template_path.exists():
            raise ValueError(f'Template does not exist: {template_path}')

        with open(template_path, 'r') as t:
            template = json.load(t)

        assert 'extra_fields' in template
            
        _validate_extra_fields(form['extra_fields'],
                               template['extra_fields'],
                               validate_values=['type', 'allow_multi_values',
                                                'blank_value_on_duplicate'])

    print('Validation successful')
    return True


def validate_experiment_against_template(experiment_json, template_json):
    """
    Validate a Elab experiment against an Elab template

    Parameters
    ----------
    experiment_json: path
        path to the record json of that instrument
    template_json: path
        path to the template json of an instrument

    Returns
    -------
    True

    Raises
    ------
    ValueError in case of failing validation
    """

    with open(experiment_json, 'r') as e:
        experiment = json.load(e)
    with open(template_json, 'r') as t:
        template = json.load(t)

    assert 'extra_fields' in template
    assert 'extra_fields' in experiment
    
    _validate_extra_fields(experiment['metadata']['extra_fields'],
                           template['extra_fields'],
                           validate_values=['type', 'options',
                                            'allow_multi_values',
                                            'blank_value_on_duplicate'])

    # TODO: Add validation of values against choices
    return True


if __name__ == '__main__':
    pass
