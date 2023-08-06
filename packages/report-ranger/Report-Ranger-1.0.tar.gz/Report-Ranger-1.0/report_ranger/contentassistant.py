from uuid import uuid4
import re
import logging

log = logging.getLogger(__name__)


class ContentAssistant:
    def __init__(self):
        self.defaultcounter = 0
        self.counters = {}
        self.defaulttable = []
        self.tables = {}
        self._register = {}
        self._table_register = {}  # For holding table formatting

    def _display_table(self, of, tablename="", *args, **kwargs):
        """ Display a table from
        """
        if tablename == "":
            table = self.defaulttable
        elif not isinstance(tablename, str):
            log.warn(
                "CA table name you're trying to display to is not a string, skipping: {}".format(tablename))
            return ""
        elif tablename not in self.tables:
            log.warning(
                "Table {} has not had any rows added to it. Skipping the display of this table.".format(tablename))
            return ""
        else:
            table = self.tables[tablename]

        return of.table(table, *args, **kwargs)

    def _register_ca(self, function, *args, **kwargs):
        """ Add a function to the register. This can be called later so that we can display content on the second pass
        """
        newuuid = str(uuid4())
        self._register[newuuid] = {
            'function': function, 'args': args, 'kwargs': kwargs}
        return newuuid

    def _register_formattable(self, *args, **kwargs):
        """ Add a function to the register. This can be called later so that we can display content on the second pass
        """
        newuuid = str(uuid4())
        self._table_register[newuuid] = {'args': args, 'kwargs': kwargs}
        return newuuid

    def parse_register(self, of, markdown):
        """ Go through the register and print out the results of the functions
        """
        log.info("Adding Content Assistant content")

        # CA register
        for uuid, f in self._register.items():
            output = f['function'](
                of, *f['args'], **f['kwargs'])
            markdown = markdown.replace(uuid, output)

        t_r_row = r'\|?([^\|\r\n]+\|)+[^\|\r\n]*'
        t_r_header_sep = r'\|?(\:?\s+-+\s*\:?\s*\|)*\s*'
        table_regex = r'[\r\s\n]*((' + t_r_row + \
            r')?[\r\s\n]*(' + t_r_header_sep + \
            r')?([\r\s\n]*' + t_r_row + ')+)'

        # Table register
        for uuid, f in self._table_register.items():
            m = re.search(uuid + table_regex, markdown)
            if not m:
                log.warn(
                    "Table formatting string does not seem to be attached to a markdown table")
                markdown = markdown.replace(uuid, '')
                continue
            table_markdown = m.group(1)
            table_output = of.table(table_markdown, *f['args'], **f['kwargs'])
            start, end = m.span()
            markdown = markdown[:start] + \
                table_output + markdown[end:]

        return markdown

    def counter(self, countername=""):
        """ This function allows counters throughout the document. Multiple counters can be used by specifying counter names.
        """
        if countername == "":
            self.defaultcounter += 1
            return self.defaultcounter
        elif not isinstance(countername, str):
            log.warn("Counter name not a string: {}".format(countername))
            return 0
        else:
            if countername not in self.counters:
                self.counters[countername] = 1
                return 1
            self.counters[countername] += 1
            return self.counters[countername]

    def get_counter(self, countername=""):
        """ This function retrieves the value of the counter WITHOUT iterating it.
        """
        if countername == "":
            return self.defaultcounter
        elif not isinstance(countername, str):
            log.warn("Counter name not a string: {}".format(countername))
            return 0
        else:
            if countername not in self.counters:
                return 0
            return self.counters[countername]

    def reset_counter(self, countername=""):
        """ Reset a counter to 0
        """
        if countername == "":
            self.defaultcounter = 0
        elif not isinstance(countername, str):
            log.warn(
                "Counter name you're trying to reset is not a string, skipping: {}".format(countername))
        else:
            self.counters[countername] = 0

    def table_row(self, tablename="", row=[]):
        """ Add a row to a content assistant table, which can then be displayed with display_table
        """
        if tablename == "":
            self.defaulttable.append(row)
        elif not isinstance(tablename, str):
            log.warn(
                "CA table name you're trying to add a row to is not a string, skipping: {}".format(tablename))
        else:
            if tablename not in self.tables:
                self.tables[tablename] = []
            self.tables[tablename].append(row)
        return ""

    def table_rows(self, tablename="", rows=[]):
        """ Add multiple rows to a content assistant table
        """
        if tablename == "":
            self.defaulttable += rows
        elif not isinstance(tablename, str):
            log.warn(
                "CA table name you're trying to add rows to is not a string, skipping: {}".format(tablename))
        else:
            if tablename not in self.tables:
                self.tables[tablename] = []
            self.tables[tablename] += rows
        return ""

    def display_table(self, *args, **kwargs):
        return self._register_ca(self._display_table, *args, **kwargs)

    def format_table(self, *args, **kwargs):
        """ Format the markdown table that's below. This allows simpler syntax for fancy formatting of markdown tables, all in jinja2 templating.
        It requires two passes, with this function returning a UUID and the second pass grepping the UUID and markdown to call of.table.
        """
        return self._register_formattable(*args, **kwargs)
