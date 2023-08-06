from . import validation
from .mdread import markdown_from_file, process_template
from .outputformatter import OutputFormatter
from .latexformatter import LatexFormatter
from .htmlformatter import HTMLFormatter
from .csvformatter import CSVFormatter
from .riskassessment import RiskAssessment
from .vulnerability import VulnerabilityList
import os
import jinja2
import datetime
import logging
import traceback

log = logging.getLogger(__name__)


class Template:
    """ A Report Ranger template for building a report from a collection of markdown. """

    def __init__(self, templatefile='', templatemapper={}, defaulttemplate=''):
        self.templatefile = templatefile
        self.templatemapper = templatemapper
        self.defaulttemplate = defaulttemplate

    def _process_included_header(self, headers, includedheaders):
        """ Process the included headers using an overlay routine:
        - Don't overwrite values
        - Add new values to dicts if they're not there
        - Append to lists
        - reset values using the "reset" header
        """
        if isinstance(includedheaders, dict):
            if not isinstance(headers, dict):
                return headers

            if 'reset' in headers:
                log.info("Resetting {} in included template headers".format(
                    headers['reset']))
                if isinstance(headers['reset'], list):
                    for r in headers['reset']:
                        if isinstance(r, str):
                            if r in includedheaders:
                                del includedheaders[r]
                        else:
                            log.warning(
                                "Reset variable {} not a string, skipping".format(r))
                else:
                    log.warning(
                        "Reset list {} not a list, skipping".format(headers['reset']))

            for header in includedheaders:
                if header in headers:
                    header = self._process_included_header(
                        headers[header], includedheaders[header])
                else:
                    headers[header] = includedheaders[header]
            return headers
        elif isinstance(includedheaders, list):
            if not isinstance(headers, list):
                return headers
            headers.extend(includedheaders)
            return headers
        else:
            return headers

    # This includes the headers from another file. This is convenient for stock text, included risk assessments, etc
    def _include_markdown(self, templateheaders, templatemarkdown, templatemapper, directory=None):
        if 'include_markdown' in templateheaders:
            if not isinstance(templateheaders['include_markdown'], str):
                log.warning(
                    "include_markdown file in template is not a string, skipping")
                return templatemarkdown

            included = templateheaders['include_markdown']

            log.info("Template including markdown from {}".format(included))
            # See if it's in the template mapper
            if included in templatemapper:
                log.info("Template markdown {} in templatemapper, changing it to {}".format(
                    included, templatemapper[included]))
                included = templatemapper[included]
            elif directory:
                included = os.path.join(directory, included)

            fn, ext = os.path.splitext(included)
            if ext != ".md" and ext != ".rr":
                log.warning(
                    "File {} included in include_markdown in the template does not end in .md or .rr, skipping".format(included))
                return templatemarkdown
            if not os.path.isfile(included):
                log.warning(
                    "File {} included in include_markdown in the template does not exist, skipping".format(included))
                return templatemarkdown

            _, ntmarkdown = markdown_from_file(included)
            return ntmarkdown
        return templatemarkdown

    # This includes the headers from another file. This is convenient for stock text, included risk assessments, etc
    def _include_headers(self, headers, templatemapper, directory=''):
        if 'include' in headers:
            if isinstance(headers['include'], str):
                headers['include'] = [headers['include']]
            for included in headers['include']:
                log.info("Template including file {}".format(included))
                # See if it's in the template mapper
                if included in templatemapper:
                    log.info("Including template {} at {}".format(
                        included, templatemapper[included]))
                    included = templatemapper[included]
                elif directory:
                    included = os.path.join(directory, included)

                fn, ext = os.path.splitext(included)
                if ext != ".md" and ext != ".rr":
                    log.warning(
                        "File {} included in the template does not end in .md or .rr, skipping".format(included))
                    return headers
                if not os.path.isfile(included):
                    log.warning(
                        "File {} included in the template does not exist, skipping".format(included))
                    return headers

                includedheaders, _ = markdown_from_file(included)
                headers = self._process_included_header(
                    headers, includedheaders)

        return headers

    # If the "change_template" header is there the report can set its own template variables
    def _change_template_headers(self, templateheaders, reportheaders):
        if 'change_template' in reportheaders:
            log.info("change_template header detected")
            if not isinstance(reportheaders['change_template'], dict):
                log.warning(
                    "change_template front matter variable not a dictionary")
                return templateheaders

            # Notice this is back to front, the template itself is included into the report change_template variable
            templateheaders = self._process_included_header(
                reportheaders['change_template'], templateheaders)

        return templateheaders

    def init_template(self, templatefile, reportheaders):
        """ Initialise the template.

        The template should be in the form (variables, markdown).
        """
        log.info("Initialising template {}".format(templatefile))

        if templatefile in self.templatemapper:
            templatefile = self.templatemapper[templatefile]

        self.templatepath = os.path.abspath(
            os.path.join(os.path.curdir, templatefile))

        self.templateheaders, self.templatemarkdown = markdown_from_file(
            templatefile, False)

        # Process include_markdown

        # Get any change template headers in the reportbody and insert it into the template
        self.templateheaders = self._change_template_headers(
            self.templateheaders, reportheaders)

        # Process templatedir
        if 'templatedir' in self.templateheaders:
            templatedirfile = self.templateheaders['templatedir']
            if not isinstance(templatedirfile, str):
                log.warning(
                    "templatedir front matter variable not a string, skipping")
                self.templatedir = os.path.dirname(os.path.abspath(
                    os.path.join(os.path.curdir, templatefile)))
            else:
                if templatedirfile in self.templatemapper:
                    templatedirfile = self.templatemapper
                self.templatedir = os.path.dirname(os.path.abspath(
                    os.path.join(os.path.curdir, templatedirfile)))
        else:
            self.templatedir = os.path.dirname(os.path.abspath(
                os.path.join(os.path.curdir, templatefile)))

        # Get any includes
        self.templateheaders = self._include_headers(
            self.templateheaders, self.templatemapper, self.templatedir)

        self.templatemarkdown = self._include_markdown(
            self.templateheaders, self.templatemarkdown, self.templatemapper, self.templatedir)

        self.templateheaders['templatedir'] = self.templatedir

        self.latex_template = os.path.join(
            self.templatedir, self.templateheaders['latex']['template'])

        if 'html' in self.templateheaders:
            self.html_template = os.path.join(
                self.templatedir, self.templateheaders['html']['template'])
        else:
            self.html_template = ''

        # Initialise the risk assessment
        self.riskassessment = RiskAssessment(
            self.templateheaders['riskassessment'])
        if 'style_text' in self.templateheaders['riskassessment']:
            self.templateheaders['defaults']['ra_style_text'] = self.templateheaders['riskassessment']['style_text']

    def process_file(self, mdfile, target, docformat, output=None):
        """ Process a file with the template. Returns the processed markdown for the file.

        The target should be one of (latex, docx, pdf)
        """
        parentdir = os.path.dirname(os.path.join(os.path.curdir, mdfile))

        # Get the report
        reportheaders, reportbody = markdown_from_file(mdfile)

        # Figure out where to get the template
        if(self.templatefile != ''):  # Preference 1: If the user has directly asked for a template, use that
            # See if it's in the template mapper
            if self.templatefile in self.templatemapper:
                self.templatefile = self.templatemapper[self.templatefile]
                log.info(
                    "Supplied template found in template mapper: {}".format(self.templatefile))

            if not os.path.isfile(self.templatefile):
                log.warning(
                    "Template file does not exist, reverting to default")
                templatefile = self.defaulttemplate
            else:
                log.info("Template file provided: {}".format(
                    self.templatefile))
                templatefile = self.templatefile
        elif 'template' in reportheaders:  # Preference 2: The template is specified in the report file
            if reportheaders['template'] in self.templatemapper:
                templatefile = self.templatemapper[reportheaders['template']]
                log.info(
                    "Template file found in template mapper: {}".format(templatefile))
            else:
                log.warning("Template {} specified in report file, but it's not found in the templatemapper in config.".format(
                    reportheaders['template']))
                log.warning("Reverting to default template.")
                templatefile = self.defaulttemplate
        else:  # Preference 3: Just use the default
            templatefile = self.defaulttemplate
            log.info(
                "Default template used: {}".format(templatefile))

        self.init_template(templatefile, reportheaders)

        output_template = ''

        # Set up the appropriate output formatter
        if target == 'latex':
            of = LatexFormatter(target, self.templatedir,
                                self.templateheaders, headers=reportheaders)
            output_template = self.latex_template
        elif target == 'html':
            of = HTMLFormatter(target, self.templatedir,
                               self.templateheaders, headers=reportheaders)
            output_template = self.html_template
        elif target == 'csv':
            of = CSVFormatter(target, self.templatedir,
                              self.templateheaders, headers=reportheaders)
        else:  # Markdown formatter as default
            of = OutputFormatter(target, self.templatedir,
                                 self.templateheaders, headers=reportheaders)

        # Set up environment variables
        of.env.set_static('ra', self.riskassessment)
        of.env.set_static('templatedir', self.templatedir)

        # The title defaults to the filename without the extension
        if of.env.get('title') == None:
            log.warn("There's no title set in the front matter, the default title is the filename of {}".format(
                os.path.basename(mdfile)))
            of.env.set_variable('title', os.path.basename(mdfile))

        # Convert date to the date object
        if of.env.get('date') == None:
            # The date defaults to the last change, otherwise today
            if of.env.get('changes') != None:
                of.env.set_variable('date', of.env.get('changes')[-1][1])
                log.info("As there's no date in front matter, date of the latest change is used: {}".format(
                    of.env.get('date')))
            else:
                of.env.set_variable('date', datetime.date.today())
                log.info("As there's no date in front matter or changes, date has been set to today: {}".format(
                    of.env.get('date')))

        if of.env.get('client') == None:
            log.warning(
                "Client name is not in the report front matter. Default of [client] will be used.")
            of.env.set_variable('client', '[client]')

        if of.env.get('version') == None:
            if not of.env.get('changes') == None:
                of.env.set_variable('version', of.env.get('changes')[-1][0])
            else:
                of.env.set_variable('version', '1.0')
                log.warning(
                    "Version is not in the report front matter. Default of 1.0 will be used.")

        # Make sure that the risk assessment methodology is processed as RR markdown
        self.riskassessment.methodology_markdown = process_template(
            {}, self.riskassessment.methodology, env=of.env, name="Risk assessment methodology")

        vulnerability_validation = {}

        if 'validation' in self.templateheaders:
            if 'report' in self.templateheaders['validation']:
                validation.validate_headers(
                    self.templateheaders['validation']['report'], reportheaders, validation.default_report_validation)
            if 'vulnerability' in self.templateheaders['validation']:
                vulnerability_validation = self.templateheaders['validation']['vulnerability']

        # Get the vulnerabilities
        if of.env.get('vulndir'):
            # Resolve the vulnerability directory
            vulndir = os.path.join(os.path.dirname(
                mdfile), of.env.get('vulndir'))
            log.info("Vulnerability directory included: {}".format(vulndir))

            vulnerabilitylist = VulnerabilityList()
            try:
                vulnerabilitylist.add_from_dir(
                    vulndir, of, self.riskassessment, vulnerability_validation=vulnerability_validation)

                updated_date = of.env.get('updated_date')

                if updated_date:
                    vulnerabilitylist = vulnerabilitylist.updated(updated_date)

                of.env.set_static('vulnerabilities', vulnerabilitylist)
                of.env.set_static('vulns', vulnerabilitylist)

                # Generate vulnerability markdown
                vulnerabilitylist.generate_markdown(of.env)
            except Exception as e:
                log.warn("Error loading vulnerabilities: {}".format(e.args))
                log.warn(traceback.format_exc())
                log.warn(
                    "Error loading vulnerabilities, setting vulnerabilities as None")
                vulnerabilitylist = None
                of.env.set_static('vulnerabilities', None)
                of.env.set_static('vulns', None)

        # Render reportbody
        try:
            j2template = jinja2.Template(reportbody)
            rbrendered = j2template.render(of.env.get_env())
            of.env.set_static('reportbody', rbrendered)
        except jinja2.exceptions.TemplateSyntaxError as error:
            log.error("Jinja2 error: {} at lineno {} in reportbody for file {}".format(
                error.message, error.lineno, error.filename))
            of.env.set_static('reportbody', "")
        except Exception as error:
            log.error("Exception found in reportbody: {}".format(error.args))
            traceback.print_exc()
            log.error("Removing reportbody text")
            of.env.set_static('reportbody', "")

        return of.output(self.templatemarkdown, output_template, docformat, output, {})
