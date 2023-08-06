from .errors import InputError
import os
from pathlib import Path
import re
from jinja2 import Template
import jinja2
import yaml
import json
from .imports import import_csv, import_xlsx
import logging
from . import section

log = logging.getLogger(__name__)

yamlmatch = re.compile(r'^[\.\=\-]{3}$')
jsonmatch = re.compile(r'^\;\;\;$')


def process_included_header(headers, includedheaders):
    """ Process the included headers using an overlay routine:
    - Don't overwrite values
    - Add new values if they're not there
    - Append to lists
    """
    if isinstance(includedheaders, dict):
        if not isinstance(headers, dict):
            return headers
        for header in includedheaders:
            if header in headers:
                header = process_included_header(
                    headers[header], includedheaders[header])
            else:
                headers[header] = includedheaders[header]
        return headers
    elif isinstance(includedheaders, list):
        if not isinstance(headers, dict):
            return headers
        headers.extend(includedheaders)
        return headers
    else:
        return headers


def process_template(headers, markdown, env=None, name='', filename=''):
    try:
        template = Template(markdown)  # Start jinja2
        env.push(headers)  # Add our new headers in
        output = template.render(env.get_env())
        env.pop()  # Take away the headers

    except jinja2.exceptions.TemplateSyntaxError as error:
        log.error(
            "Error in processing {} at {}".format(name, filename))
        log.error("Message: {}. Line number: {}.".format(
            error.message, error.lineno))
        log.error("Affected lines:")
        mdlines = markdown.splitlines()
        for i in range(12):
            el = error.lineno - 7 + i
            if el < 0:
                continue
            if el >= len(mdlines):
                continue
            log.error("{}: {}".format(el, mdlines[el]))
        raise Exception("Error reading {}: {} at lineno {} ".format(name,
                                                                    error.message, error.lineno))

    return output


def _process_includes(headers, includemapper):
    if isinstance(headers['include'], str):
        headers['include'] = [headers['include']]
    for included in headers['include']:
        # Process includemapper
        if included in includemapper:
            included = includemapper[included]
        filepath = Path(included)
        cwdpath = Path(os.path.curdir)
        if cwdpath not in filepath.parents:
            log.warn(
                "include path {} doesn't seem to be in cwd".format(filepath))
            continue
        log.info("Including file {}".format(filepath))
        includedheaders, _ = markdown_from_file(included)
        headers = process_included_header(
            headers, includedheaders)
    return headers


def _process_imports(headers):
    if not isinstance(headers['import'], dict):
        log.warn("import front matter variable not a dict, skipping")
    else:
        # Begin CSV imports
        if 'sections' in headers['import']:
            sectionlist = headers['import']['sections']
            if not isinstance(sectionlist, list):
                log.warn(
                    "Section import front matter variable not a list, skipping")
            for sectionimport in sectionlist:
                if not isinstance(sectionimport, dict):
                    log.warn(
                        "Section import item in front matter not a dict, skipping")
                    continue
                if 'directory' not in sectionimport or not isinstance(sectionimport['directory'], str):
                    log.warn(
                        "Section import item does not have a directory, skipping")
                    continue
                if 'variable' not in sectionimport or not isinstance(sectionimport['variable'], str):
                    log.warn(
                        "Section import item does not have variable name, skipping")
                    continue
                if sectionimport['variable'] in headers:
                    log.warn(
                        "Section import variable name already in front matter, skipping")
                    continue
                if 'ordinal' in sectionimport:
                    ordinal = sectionimport['ordinal']
                else:
                    ordinal = '1'

                # Build the section
                newsection = section.Section(
                    sectionimport['directory'], ordinal)

                headers[sectionimport['variable']] = newsection

        # Begin CSV imports
        if 'csv' in headers['import']:
            csvlist = headers['import']['csv']
            if not isinstance(csvlist, list):
                log.warn(
                    "csv import front matter variable not a list, skipping")
            for csvimport in csvlist:
                if not isinstance(csvimport, dict):
                    log.warn(
                        "csv import item in front matter not a dict, skipping")
                    continue
                if 'file' not in csvimport or not isinstance(csvimport['file'], str):
                    log.warn(
                        "csv import item does not have file location, skipping")
                    continue
                if 'variable' not in csvimport or not isinstance(csvimport['variable'], str):
                    log.warn(
                        "csv import item does not have variable name, skipping")
                    continue
                if csvimport['variable'] in headers:
                    log.warn(
                        "csv import variable name already in front matter, skipping")
                    continue
                if 'as_dict_list' in csvimport and not isinstance(csvimport['as_dict_list'], bool):
                    log.warning(
                        'csv import defines "as_dict_list", but it is not a boolean')
                    continue
                if 'index_col' in csvimport and not isinstance(csvimport['index_col'], int):
                    log.warning(
                        'csv import defines "index_col", but it is not an integer')
                    continue

                headers[csvimport['variable']] = import_csv(csvimport['file'], as_dict_list=csvimport.get(
                    'as_dict_list'), index_col=csvimport.get('index_col'))
        # Begin xlsx imports
        if 'xlsx' in headers['import']:
            xlsxlist = headers['import']['xlsx']
            if not isinstance(xlsxlist, list):
                log.warn(
                    "xlsx import front matter variable not a list, skipping")
            for xlsximport in xlsxlist:
                if not isinstance(xlsximport, dict):
                    log.warn(
                        "xlsx import item in front matter not a dict, skipping")
                    continue
                if 'file' not in xlsximport or not isinstance(xlsximport['file'], str):
                    log.warn(
                        "xlsx import item does not have file location, skipping")
                    continue
                if 'variable' not in xlsximport or not isinstance(xlsximport['variable'], str):
                    log.warn(
                        "xlsx import item does not have variable name, skipping")
                    continue
                if xlsximport['variable'] in headers:
                    log.warn(
                        "xlsx import variable name already in front matter, skipping")
                    continue
                if 'as_dict_list' in xlsximport and not isinstance(xlsximport['as_dict_list'], bool):
                    log.warning(
                        'xlsx import defines "as_dict_list", but it is not a boolean')
                    continue
                if 'index_col' in xlsximport and not isinstance(xlsximport['index_col'], int):
                    log.warning(
                        'xlsx import defines "index_col", but it is not an integer')
                    continue

                headers[xlsximport['variable']] = import_xlsx(
                    xlsximport['file'],
                    xlsximport.get('worksheet'),
                    xlsximport.get('min_row'),
                    xlsximport.get('max_row'),
                    xlsximport.get('min_col'),
                    xlsximport.get('max_col'),
                    as_dict_list=xlsximport.get('as_dict_list'),
                    index_col=xlsximport.get('index_col')
                )

    return headers


def markdown_from_file(file_loc, env=None, process_includes=True, includemapper={}, process_imports=True):
    """ Read the markdown from a file.

    Arguments:
    - file_loc: The location of the file to read

    Returns (headers, markdown) where headers is a dict and markdown is a long string """

    log.debug("Reading markdown from file {}".format(file_loc))

    if not os.path.exists(file_loc):
        log.warn("Trying to read file {} but it doesn't exist".format(file_loc))
        return dict(), ""

    with open(file_loc, 'r') as vf:
        # If the first line starts with "---" that's our headers We have to make sure that it starts with "---"
        firstline = vf.readline()
        headers = dict()
        if yamlmatch.match(firstline):
            line = vf.readline()
            headerstring = ''
            # Read the headers.
            # Go until we get to the terminator to end the headers
            while not yamlmatch.match(line):
                headerstring += line
                line = vf.readline()
                if not line:
                    raise InputError(
                        'Markdown file {} YAML headers don\'t end in a YAML terminator (...,---,===)'.format(file_loc))
            headers = yaml.safe_load(headerstring)  # Retrieve the YAML headers
            if headers == None:
                headers = {}
            markdown = vf.read()  # Read the rest of the file
        elif jsonmatch.match(firstline):
            line = vf.readline()
            headerstring = ''
            # Read the headers.
            # Go until we get to the terminator to end the headers
            while not jsonmatch.match(line):
                headerstring += line
                line = vf.readline()
                if not line:
                    raise InputError(
                        'Markdown file {} JSON headers don\'t end in a JSON terminator (;;;)'.format(file_loc))
            headers = json.loads(headerstring)  # Retrieve the JSON headers
            markdown = vf.read()  # Read the rest of the file
        else:
            # There's no headers in this file. Put the first line back and just add it all into the markdown
            markdown = firstline + '\n' + vf.read()

        # Begin post processing. Process includes and imports.

        # Process includes in headers
        if process_includes and 'include' in headers:
            headers = _process_includes(headers, includemapper)

        # Process imports in headers
        if process_imports and 'import' in headers:
            headers = _process_imports(headers)

        return headers, markdown


def markdown_from_directory(dir_loc):
    log.debug("Reading markdown from directory {}".format(dir_loc))

    if not os.path.isdir(dir_loc):
        raise InputError("dir_loc:{0} is not a valid path".format(dir_loc))

    files = []

    for f in os.listdir(dir_loc):
        mdfile = os.path.join(dir_loc, f)
        if os.path.isfile(mdfile):
            fn, ext = os.path.splitext(mdfile)
            if ext == ".md" or ext == ".rr":
                files.extend([markdown_from_file(mdfile)])

    return files
