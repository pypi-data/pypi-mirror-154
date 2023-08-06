from .outputformatter import OutputFormatter
import re
import mistune
from .csvrenderer import CSVRenderer
from .table import Table
import logging
import csv
from tabulate import tabulate

log = logging.getLogger(__name__)

csv_defaults = {
    'columns': {
        'Section': 'section',
        'Name': 'name',
        'Risk': 'risk',
        'Details': 'markdown'
    }
}

header_aliases = {
}


class CSVFormatter(OutputFormatter):
    def __init__(self, format="csv", templatedir='', template=dict(), headers=dict()):
        OutputFormatter.__init__(self, "csv", templatedir, template, headers)
        self.figformat = "png"
        csvoptions = {}
        csvoptions.update(csv_defaults)
        if 'csv' in template:
            csvoptions.update(template['csv'])

        self.columns = csvoptions['columns']

    def escape(self, text):
        ''' Escape the given text based on the format we're working with

        :param text: a plain text message
        :return: the message escaped to appear correctly in CSV
        '''
        conv = {
            '\'': r'\'\''
        }
        regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(
            conv.keys(), key=lambda item: - len(item))))
        return regex.sub(lambda match: conv[match.group()], text)

    def table(self, table, options={}, **tableargs):
        ''' This function formats the table in either latex or markdown, depending on the output.'''

        t = Table(table, env=self.env, **tableargs)

        # We're going to do a markdown table with tabulate
        colalign = t.colalign
        # We need to convert the 'l' and 'r' in colalign if it exists
        for col in range(len(colalign)):
            if colalign[col] == 'l':
                colalign[col] = 'left'
            elif colalign[col] == 'c':
                colalign[col] = 'center'
            elif colalign[col] == 'r':
                colalign[col] = 'right'
            else:
                colalign[col] = ''

        if len(header) == 0:
            return tabulate(t.table, stralign=colalign, tablefmt="github")
        else:
            return tabulate(t.table[1:], t.table[0], stralign=colalign, tablefmt="github")

    def headers(self):
        return ''

    def output(self, templatemarkdown, templatefile='', docformat='csv', outputfile='', options={}):
        """ Output vulnerability details to CSV.

        This involves getting the vulnerabilities, splitting the content between vulnerability headings, stripping formatting, and outputting into CSV.
        """

        # Get vulnerability information

        rows = []
        rows.append(list(self.columns.keys()))

        vuln_list = self.env.get('vulnerabilities')
        for section in vuln_list.sections:
            for vuln in section.vulnerabilities:
                lr = CSVRenderer()
                lrm = mistune.create_markdown(renderer=lr)

                potcols = {}
                markdown = vuln.markdown
                mardown_rendered = lrm(markdown)
                potcols['markdown'] = mardown_rendered
                potcols.update(lr.heading_text)
                potcols.update(vuln.headers)
                potcols['section'] = section.name

                row = []
                for col in self.columns:
                    if self.columns[col] in potcols:
                        row.append(potcols[self.columns[col]])
                    else:
                        row.append('')
                rows.append(row)

        log.info("Writing CSV file")
        with open(outputfile, 'w') as fh:
            csvw = csv.writer(fh)
            csvw.writerows(rows)

        return rows
