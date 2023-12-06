from rich import print
from argparse import ArgumentParser
import sys
import os


class DrBuilder:
    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument("-p", "--payload", dest="payload", help="Use the payload")
        self.parser.add_argument("--lhost", dest="lhost", help="Using local host")
        self.parser.add_argument("--lport", dest="lport", help="Using local port")
        self.parser.add_argument("-e", "--encrypt", dest="encrypt", action="store_true", help="Using encryption")
        self.parser.add_argument("-o", "--output", dest="output", help="Output the payload")

        self.payload = None
        self.lhost = None
        self.lport = None
        self.encrypt = False
        self.output = None

    def build_payload(self):
        payload_path = os.path.abspath(self.payload)
        if os.path.exists(payload_path):
            with open(payload_path, "r") as payload_file:
                payload_content = payload_file.read()
                print("[bold blue]Payload Content:[/bold blue]")
                print(payload_content)
        else:
            print("[bold red]Payload file not found.[/bold red]")

        print("[bold green]Building payload...[/bold green]")
        print(f"Payload: [cyan]{self.payload}[/cyan]")
        print(f"LHOST: [cyan]{self.lhost}[/cyan]")
        print(f"LPORT: [cyan]{self.lport}[/cyan]")
        if self.encrypt:
            print("[yellow]Encryption enabled[/yellow]")
        if self.output:
            print(f"Output: [cyan]{self.output}[/cyan]")
        else:
            print(f"Output: [cyan]{os.getcwd()}[/cyan]")

    def help(self):
        self.parser.print_help()

if __name__ == "__main__":
    builder = DrBuilder()

    # args = ["-p", "windows/x64/reverse_tcp", "--lhost", "192.818.184.1", "--lport", "4444"]

    args = sys.argv[1:]  # تجاهل اسم البرنامج نفسه


    options = builder.parser.parse_args(args)
            
    if options.payload and options.lhost and options.lport:
        builder.payload = options.payload
        builder.lhost = options.lhost
        builder.lport = options.lport
        builder.encrypt = options.encrypt
        builder.output = options.output
        builder.build_payload()
    else:
        print("[bold red]Missing required options. Use 'help' for assistance.[/bold red]")
