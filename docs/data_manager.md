## Instructions for Data Managers

### Why use Diglabtools

Diglabtools permits the definition of survey forms for metadata collection independently of a specific platform use to serve the form. At the moment DigLabtools support RedCap as well as ElabFTW, but more server backend can be integrated in the future.
By using Diglabtools surveys can be built from a set of existing survey templates (see the [ElabFTW template parts](../../../elab_bridge/template_parts) and [RedCap template parts](../../../redcap_bridge/template_parts). Templates can be translated between the bridge modules using the [conversion module](../../../diglab_utils/conversion.py))
Organizing the survey form specifications outside of a server environment has the advantage that a survey can be set up based on pure text files, which can easily be version controlled, e.g. using git. Using version control the generation of a survey form can be provenance tracked, as already implemented for the redcap_bridge.
Another advantage of DigLabTools is that the use of templates permits standardization of survey forms across different projects, but splitting generic templates and project specific customizations.

_Note:_ RedCap surveys specifications contain a superset of ElabFTW survey specifications. When converting from RedCap to ElabFTW some parts of the specifications will be ignored.


### Creating a project

The specifications of a project require 3 files:

- `project.json`: This file defines the general settings of the project. It contains reference to the files defining the survey content (by convention called `structure.json` and `customization.json`), the credentials to connect to the server and potentially a list of survey templates against which the project can be validated.
- `structure.tsv/json`: This file defines the fields present in the survey form. Currently this is in `tsv` format for RedCap projects and `json` for ElabFTW projects. In the simplest case of only using a survey template, this mostly consists of the name of the template to include
- `customizations.tsv/json`: This file defines project specific customization of the survey fields included via the `structure.tsv/json`. This is e.g useful to provide a selection of values for a predefined field, like the names of the experiments for the `User` field.

For more examples on how a project can be set up, see the projects used in the [elab tests](../../../elab_bridge/tests/testfiles_elab/TestProject) and [redcap tests](../../../redcap_bridge/tests/testfiles_redcap/TestProject) 

To get from the project specification files listed above to a survey form on a server multiple steps are required

1) [Server Project Setup] Generation of an empty project on the server
2) [Local Project Setup] Generation of the project specification files above (see also the [user level setup](setup.md))
3) [Survey Generation] Using the elab_bridge / redcap_bridge `project_control.setup_project()` function.

The last step will perform multiple steps internally:
- building of the general project survey form based on the `structure` specifications using the `project_building.build_project` function
- customization of the project survey based on the `customization` specification using the `project_building.customize_project` function
- upload of the project survey to the server using the `server_interface` module

### Running tests

Running the tests of DigLabTools requires `pytest` to be installed and generation of an empty project on the server to be used for upload and download testing.
Instead of adding the server api token to the TestProject configuration file, create an environment variable named `ELAB_API_TOKEN` / `REDCAP_API_TOKEN` containing the coresponding token. This will be automatically used while running the tests.


