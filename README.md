# DigLabTools

*DigLabTools* is a collection of libraries with digital labbook functionalities.

The main functionality of *DigLabTools* to facilitate the generation and standardization of surveys for metadata collection. It permits the generation of surveys based on templates and provides a framework for reproducible assembly and customization of surveys. In addition it provides a simple command line interface to retrieve the collected data from metadata server. 

*DigLabTools* supports two types of servers for metadata collection: *RedCap* and *eLabFTW*.


For both types of servers the main *DigLabTools* features are:

- **Template based** survey generation for standardized survey layouts
- **Inherent provenance tracking** for reproducible survey generation
- **Python interface** for generation of surveys and setup on a the metadata server
- **Command line interface** for quick data (record) retrieval from the metadata server
- **Compression of data** to improve readability of retrieved data

These functionalities are implemented in the *RedCapBridge* and *ElabBridge* modules, correspondingly.

Important links
---------------

- Official documentation: https://diglabtools.readthedocs.io