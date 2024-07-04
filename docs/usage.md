## Usage

### Downloading metadata

To download the metadata of a project you can use the command line tool `RedCapBridge` or `ElabBridge`, depending on your choice of metadata server. Use the `RedCapBridge --help` (or `ElabBridge --help`) to learn more about the different functions that the server interface offers.

### Building projects

The functions for project building, validation and control are only accessible via Python. Read the module documentation to learn more about these methods.

### Download Function

To download your experiments from eLab, follow the procedure below.

1. After completing the **installation** module, go to your terminal
2. Enter the following command:
`ElabBridge extended_download output_file_path config_file_path tag -f csv `
3. `output_file_path` is the **complete** path to your csv file where your experiments will be saved
4. `config_file_path` is the path to your `.json` file containing your API key as seen above
