# DigLabTools
This repository contains tools to interact with the DigLab metadata collection standard. There are two approaches available for this, the original `DigLab` PDF approach and a server based approach based on RedCap.

To be able to access the metadata from a RedCap server an API token needs to be created.
# Install the api key

Go to the  ```redcap_bridge``` folder and create a copy of the file ```config_template.yaml``` called ```config.yaml```
```
>cd redcap_bridge
>cp config_template.yaml config.yaml

```

and replace the API token with the one provided by the RedCap server in ```config.yaml```.
