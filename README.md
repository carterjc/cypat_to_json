# cypat_to_json
Working repository that scrapes the public CyberPatriot scoreboard and generates a complete JSON file.

# Synopsis
This program will generate a detailed JSON file that can be used as one pleases. Be warned, this program takes a particularly long time to run (especially in the early rounds) because it makes thousands of individual GET requests to discover individual image information.
Note that this program is very similar to cypat_to_excel except in the format and the inclusion of periodic image score data.

# How to Run
First, clone the repository:
`git clone https://github.com/carterjc/cypat_to_json.git`

Navigate to the folder:
`cd cypat_to_json`

Ensure the following modules are installed:
- json
- bs4
- requests

If needed, use: `pip install ______` (module)

Run the script with `python main.py` and enter accurate data into the requested fields.

After a bit of waiting, enjoy!
