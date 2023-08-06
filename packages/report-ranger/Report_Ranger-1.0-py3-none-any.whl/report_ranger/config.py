import os

# This is to fill in the defaults so there's not too many variables
config = {
    "defaulttemplate": os.getenv('RR_TEMPLATE', '/template/volkis-template.yaml'),
    "input_file": os.getenv('RR_INPUT_FILE', "/report/reportbody.md"),
    "output_file": os.getenv('RR_OUTPUT_FILE', '-'),
    "nessusmapper": os.getenv('RR_NESSUSMAPPER', ''),
    "format": os.getenv('RR_FORMAT', ""),
    "verbose": os.getenv('RR_VERBOSE', False),
    # The template mapper. This gives the locations of template files for each template.
    "templatemapper": {
    },
    # Files with additional parameters
    "includes": []
}
