# DigLabTools

DigLabTools is a collection of tools to interact with the DigLab metadata collection standard based on RedCap surveys.

## Installation

To use DigLabTools you need to have a Python installation available on your computer including the `pip` package.
You can install DigLabTools from PyPI via `pip install DigLabTools`.
Note that DigLabTools requires git. If git is not available on your system you can install it manually. When using conda this can be done via `conda install -c anaconda git`.

### Generate an API token

To be able to access the metadata from a RedCap server an API token needs to be created. For this login to your local RedCap server and go to the `API` menu on the left pane. Here you can generate a personalized access token for your user account. Copy the generated token, you will need to add it to your DigLab project configuration in the next step.

### Configure your DigLab project

You need to create a project configuration `json` file on your computer to store the RedCap API token you just generated. Use your preferred text editor to create a `<project_name>.json` file with the following content:

```
{
  "structure": "structure.csv",
  "customization": "customization.csv",
  "validation": [],
  "api_token": "<paste your API token here>",
  "api_url": "<put the url of your RedCap server here>/api/"
}
```

Replace the `<...>` entries with the corresponding values for your project. The `structure`, `customization` and `validation` entries are required for project building and not needed to download the collected metadata.

## Usage

### Downloading metadata

To download the metadata of a project you can use the command line tool `RedCapBridge`. Use the `RedCapBridge --help` to learn more about the different functions that `RedCapBridge` offers.

### Building projects

The functions for project building, validation and control are only accessible via Python. Read the module documentation to learn more about these methods.
