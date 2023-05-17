## Setup

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
Note that the API URL should come in the `https://redcap.MY_INSTIUTION.org` format.
