## Setup

### Generate an API token

To be able to access the metadata from a server an API token needs to be created. 

#### ...on RedCap
Login to your local RedCap server and go to the `API` menu on the left pane. Here you can generate a personalized access token for your user account. Copy the generated token, you will need to add it to your DigLab project configuration in the next step.

![RedCap_API-token-generation.png](images/RedCap_API-token-generation.png)

#### ...on eLabFTW
Login to your local eLabFTW server and go to your `User Control Panel`. Switch to the `API KEYS` tab and generate a personalized API Key. Note that this key will only be displayed once. If you only plan to use DigLabTools to retrieve data from the metadata server, choose the `Read Only` permission. In case you also want to generate surveys via DigLabTools, choose `Read/Write` permissions.  Copy the generated key and use it as `api_token` in your DigLab project configuration in the next step.

![ElabFTW_API-token-generation.png](images/ElabFTW_API-token-generation.png)

### Configure your DigLab project

You need to create a project configuration `json` file on your computer to store the API token you just generated. You can download a template of that files [here](config_template.json) or use your preferred text editor to create a `<project_name>.json` file with the following content:

```
{
  "title": "<My Project Title>",
  "structure": "structure.csv",
  "customization": "customization.csv",
  "validation": [],
  "api_token": "<paste your API token here>",
  "api_url": "<put the url of your metadata server here>",
}
```

Replace the `<...>` entries with the corresponding values for your project. The `structure`, `customization` and `validation` entries are only required for project building and not needed to download the collected metadata.
Note that the API URL format depends on the server you are using:

| Server   | API URL Format                           |
|----------|------------------------------------------|
| RedCap   | `https://redcap.MY_INSTIUTION.org/api/`  |
| ElabFTW  | `https://MY_INSTITUTION.elab.one/api/v2` |
