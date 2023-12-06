import os
from rich.table import Table
from rich.console import Console
from optparse import OptionParser
import sys

console = Console()

def usage():
    console.print(
        """
command

    -s --services         the services tool
    -u --update         update database DrSploit
    -v --version         show the version
    -h --help         show this banner help
Using :
    drdb <command>

Example :
    drdb -u""",
        style="bold",
    )
    sys.exit()


class Helpe:
    @staticmethod
    def usage():
        usage()


class DrSploit:
    def __init__(self):
        self.services = None
        self.update = None
        self.virsun = False

        self.parser = OptionParser(add_help_option=False, epilog="drsploit")
        self.parser.add_option(
            "-s", "--services", dest="services", help="Start Services Sql DataBase"
        )
        self.parser.add_option(
            "-u", "--update", type="str", dest="update", help="Update DrSploit"
        )
        self.parser.add_option(
            "-h", "--help", dest="help", action="store_true", help="help DrSploit"
        )
        self.parser.add_option(
            "-v",
            "--virsun",
            dest="virsun",
            action="store_true",
            help="DrSploit Virsun",
        )

    def parse_args(self):
        (opts, _) = self.parser.parse_args()

        if opts.help:
            Helpe.usage()
        elif opts.virsun:
            console.print("DrSploit 1.0v", style="bold")
            sys.exit()

        self.services = opts.services
        self.update = opts.update
        self.virsun = opts.virsun


if __name__ == "__main__":
    drsploit = DrSploit()
    drsploit.parse_args()

    # يمكنك استخدام متغيرات drsploit.services و drsploit.update و drsploit.virsun هنا حسب الحاجة.
