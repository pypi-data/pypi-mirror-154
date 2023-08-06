from . import vulnerability
from . import config  # Configuration settings within report ranger
from .errors import InputError
from .template import Template
import os
import jinja2
import logging

log = logging.getLogger(__name__)


def main(args):
    # Turn on verbose mode
    if args.verbose:
        logging.basicConfig(
            format='%(levelname)s: %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s',
                            level=logging.WARNING)

    parentdir = os.path.dirname(os.path.join(os.path.curdir, args.input))

    # We need to change the current working directory to the directory of the template otherwise relative
    # paths inside the template won't work. For instance you won't be able to include executivesummary.md
    rr_parent_folder = os.path.abspath(os.path.curdir)

    # Get the absolute location of the template so it survives the change of directory

    if args.template:
        if args.template in config.config['templatemapper']:
            templatefile = config.config['templatemapper'][args.template]
        else:
            templatefile = os.path.abspath(args.template)
    else:
        templatefile = ''

    os.chdir(parentdir)
    parentdir = '.'
    mdfile = os.path.basename(args.input)

    # Get the template
    template = Template(
        templatefile, config.config['templatemapper'], config.config['defaulttemplate'])

    # Get the extension of the output file
    fn, ext = os.path.splitext(args.output)

    # Figure out what target we have
    if args.format == "pdf":
        target = "latex"
        docformat = "pdf"
    elif args.format == "latex":
        target = "latex"
        docformat = "markdown"
    elif args.format == "markdown":
        target = "markdown"
        docformat = "markdown"
    elif args.format == "docx":
        target = "docx"
        docformat = "docx"
    elif args.format == "html":
        target = "html"
        docformat = "html"
    elif args.format == "csv":
        target = "csv"
        docformat = "csv"
    else:
        if ext == ".docx":
            target = "docx"
            docformat = "docx"
            log.info("Setting target and format to docx")
        elif ext == ".md" or ext == ".rr":
            target = "markdown"
            docformat = "md"
            log.info("Setting target to markdown and format to md")
        elif ext == ".html":
            target = "html"
            docformat = "html"
            log.info("Setting target and format to html")
        elif ext == ".csv":
            target = "csv"
            docformat = "csv"
            log.info("Setting target and format to csv")
        else:  # Default to PDF
            target = "latex"
            docformat = "pdf"
            log.info("Setting target to latex and format to pdf")

    # Pandoc does not support PDF output to stdout, so we need to hack it by
    # making a symlink to /dev/stdout and outputting to that file
    stdout_link = None
    if docformat.lower() == 'pdf' and args.output == '-':
        stdout_link = '/tmp/stdout.pdf'
        os.symlink('/dev/stdout', stdout_link)
        args.output = stdout_link

    # Convert output file path into full path if relative path is given
    if args.output[0] != '/':
        args.output = os.path.join(rr_parent_folder, args.output)

    try:
        output = template.process_file(mdfile, target, docformat, args.output)
    except InputError as ie:
        log.error("Input Error: {}".format(ie.message))
        exit()
    except jinja2.exceptions.TemplateSyntaxError as error:
        log.error("Jinja2 error: {} at lineno {} for file {}".format(
            error.message, error.lineno, error.filename))
        exit()

    # If we're outputting to stdout, remove the link
    if stdout_link and os.path.exists(stdout_link):
        os.remove(stdout_link)
