#!/usr/bin/python3

import sys
import os
import time
import cmd
import rich
from pydoc import importfile
from rich.table import Table
from rich.console import Console 
from rich.live import Live
from optparse import OptionParser
from typing import IO
import platform
from db.sortPaths import Sort
from scripts.banners import sem
from db.utils import search_json
import subprocess
from terminaltables import AsciiTable


# الآن يمكن استخدام الوظائف والكائنات من module_name


"""

    Welcome To DrSploit v1

"""

c = cmd
services = ""
#quiet = ""
help = "" 
update = ""
virsun = True
console = Console()


PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'


class DRConsole(c.Cmd):
    def __init__(self,read=None, completekey: str = "tab", stdin: IO[str] | None = None, stdout: IO[str] | None = None) -> None:
        super().__init__(completekey, stdin, stdout)
        self.prompt = "\033[4mdr >\033[0m"
        self.read = read
        self.S = Sort()
        self.readjson = self.S.readJsonFile()
        self.readDirs = self.S.readDirs()
        self.rhostg = ""
        self.module = None
        self.used: type[dict] = dict
        self.data = {}
        self.moduleIndex: type[list] = list
        self.used_module = None
        self.workspaces = {}
        self.workspaces['default'] = []
        self.current_workspace = None
        self.active_sessions = {'0':"windows"}
        self.global_options = {
            "ConsoleLogging": False,
            "LogLevel": 0,
            "MeterpreterPrompt": "meterpreter",
            "MinimumRank": 0,
            "Prompt": "msf6",
            "PromptChar": ">",
            "PromptTimeFormat": "%Y-%m-%d %H:%M:%S",
            "SessionLogging": False,
            "SessionTlvLogging": False,
            "TimestampOutput": False
        }
        self.hosts = [
            {
                "address": "92.204.136.214",
                "mac": "00:11:22:33:44:55",
                "name": "device",
                "os_name": "Symbian",
                "os_flavor": "",
                "os_sp": "",
                "purpose": "",
                "info": "",
                "comments": ""
            },
            {
                "address": "204.92.214.1",
                "mac": "00:AA:BB:CC:DD:EE",
                "name": "OS",
                "os_name": "",
                "os_flavor": "",
                "os_sp": "",
                "purpose": "",
                "info": "",
                "comments": ""
            }
        ]
        self.workspaces = [
            {
                "name": "default",
                "hosts": 7,
                "services": 36,
                "vulns": 3,
                "creds": 4,
                "loots": 0,
                "notes": 14
            },
            {
                "name": "kurimibank",
                "hosts": 1,
                "services": 1,
                "vulns": 0,
                "creds": 0,
                "loots": 0,
                "notes": 0
            }
        ]
        self.current_workspace = "default"
        self.services = [
            {
                "host": "92.204.214",
                "port": 21,
                "proto": "tcp",
                "name": "ftp",
                "state": "open",
                "info": ""
            }
        ]
        self.vulns = [
            {
                "timestamp": "2023-07-14 19:35:36 UTC",
                "host": "192.168.146.128",
                "name": "VSFTPD v2.3.4 Backdoor Command Execution",
                "references": "OSVDB-73573,URL-http://pastebin.com/AetT9sS5,URL-http://scarybeastsecurity.blogspot.com/2011/07/alert-vsftpd-download-backdoored.html"
            },
            {
                "timestamp": "2023-07-16 18:55:01 UTC",
                "host": "192.168.146.128",
                "name": "SSH Login Check Scanner",
                "references": "CVE-1999-0502"
            },
            {
                "timestamp": "2023-07-16 20:15:45 UTC",
                "host": "192.168.146.128",
                "name": "Telnet Login Check Scanner",
                "references": "CVE-1999-0502"
            }
        ]
        self.creds = [
            {
                "host": "192.168.146.128",
                "origin": "192.168.146.128",
                "service": "21/tcp (ftp)",
                "public": "user",
                "private": "user",
                "realm": "",
                "private_type": ""
            }
        ]
        self.loot = [
            {
                "host": "",
                "service": "",
                "type": "",
                "name": "",
                "content": "",
                "info": "",
                "path": ""
            }
        ]
        self.notes = [
            {
                "Time": "2023-07-14 19:32:29 UTC",
                "Host": "192.168.146.128",
                "Service": "",
                "Port": "",
                "Protocol": "",
                "Type": "host.os.nmap",
                "Data": "{:os_vendor=>\"Actiontec\", :os_family=>\"embedded\", :os_version=>nil, :os_accuracy=>100, :os_match=>\"DD-WRT v24-sp2 (Linux 2.4.37)\"}"
            }
        ]


    def default(self,line):
        self.exec(line)
        

    def pprompt(self,line):
        self.prompt = line

       
                
                    
    def exec(self,command):

        if platform.system() == "Windows":
            # try:
            #     # تنفيذ الأمر والتقاط الإخراج
            #     subprocess.run(command,capture_output=True,  check=True)

            #     print(f"The command '{command}' exists in the system.")
            # except subprocess.CalledProcessError:
            #     print(f"The command '{command}' does not exist in the system.")
            if os.system(f"where {command} > nul 2>&1") == 0:
                print("x")
            else:
                print("Command Not Found")
        else:
            if os.system("command -v %s >/dev/null"%(command)) == 0:
                print("exec:",command)
                x = os.system(command)
                print(x)
            else:
                print("Command Not Found")


    def do_info(self, arg):
        args = arg.split()
        if not args:
            print("Usage: info <module name> [mod2 mod3 ...]\n")
            print("Options:")
            print("* The flag '-j' will print the data in json format")
            print("* The flag '-d' will show the markdown version with a browser. More info, but could be slow.")
            print("Queries the supplied module or modules for information. If no module is given,")
            print("show info for the currently active module.")
            return
        
        modules = args
        json_format = "-j" in modules
        markdown_format = "-d" in modules
        if json_format:
            modules.remove("-j")
        if markdown_format:
            modules.remove("-d")

        for module in modules:
            self.print_module_info(module, json_format, markdown_format)

    def print_module_info(self, module, json_format, markdown_format):
        print(f"Module: {module}")
        # Retrieve and print module information
        if json_format:
            print(f"Info in JSON format for {module}")
        elif markdown_format:
            print(f"Info in Markdown format with a browser for {module}")
        else:
            print(f"Info for {module}")

    def help_info(self):
        help_text = """
Usage: info <module name> [mod2 mod3 ...]

Options:
* The flag '-j' will print the data in json format
* The flag '-d' will show the markdown version with a browser. More info, but could be slow.
Queries the supplied module or modules for information. If no module is given,
show info for the currently active module.
        """
        print(help_text)

    def complete_info(self, text, line, begidx, endidx):
        """مكمل للأمر hello."""
        options = ['all']
        if text:
            completions = [option for option in options if option.startswith(text)]
        else:
            completions = options
        return completions

    def do_show(self,args):
        if args in ['all', 'exploits', 'options','post','auxiliary','favorites','payloads','encoders','nops','plugins']:
            
            print("\n",args.capitalize(),sep="")
            print("="*len(args),end="\n\n")
            var = self.S.listpath("./modules/"+args)
            
            table = Table()
            table.add_column("#")
            table.add_column("Name")
            table.add_column("Disclosure Date")
            table.add_column("Rank")
            table.add_column("Check")
            table.add_column("Description")

            S = Sort()
            Dicts = self.readjson
            with Live(table, refresh_per_second=4) as live:  # update 4 times a second to feel fluid
                x = 0
                for i in Dicts:
                    if i in var:
                        table.add_row(str(x),Dicts[i]['name'],Dicts[i]['date'],"nurmal","no",Dicts[i]['description'])
                        x += 1




    def complete_show(self, text, line, begidx, endidx):
        """مكمل للأمر hello."""
        options = ['all', 'exploits', 'options','post','auxiliary','favorites','payloads','encoders','nops','plugins']
        if text:
            completions = [option for option in options if option.startswith(text)]
        else:
            completions = options
        
        # إضافة مكمّلات إضافية عند استخدام "use"
        if self.used_module is not None:
            module_completions = ['options', 'info']
            completions = [option for option in module_completions if option.startswith(text[len("show " + self.used_module):])]

        return completions

    def do_use(self,args):
        try:
            int(args)
            self.moduleIndex = 0
            if int(args) in self.moduleIndex:
                file_path = './modules/auxiliary/scanner/example.py'
                if platform.system() == "Windows":
                    inps = ((file_path.replace("./modules/","")).rsplit("/"))
                else:
                    inps = ((file_path.replace("./modules/","")).rsplit("/"))
            else:
                console.print("[red][-][white] Invalid module index:")
            self.module = importfile(file_path)
            inps[-1] = inps[-1].replace(".py","")
            inps = "%sdr%s %s(%s%s"%(UNDERLINE,END,inps[0],RED,BOLD)+ "/".join(inps[1:])+"%s) >"%(END)
            self.pprompt(line=inps)
            self.used_module = "True"
        except:
            file_path = "./modules/"+args+".py"
            if platform.system() == "Windows":
                inps = ((args.replace("./modules/","")).rsplit("/"))
            else:
                inps = ((args.replace("./modules/","")).rsplit("/"))   

            self.module = importfile(file_path)
            inps[-1] = inps[-1].replace(".py","")
            inps = "%sdr%s %s(%s%s"%(UNDERLINE,END,inps[0],RED,BOLD)+ "/".join(inps[1:])+"%s) >"%(END)
            self.pprompt(line=inps) 
            self.used_module = "True"


        
    def do_run(self,args):
        if self.module is not None:
            self.module.hii()
        

    def complete_use(self, text, line, begidx, endidx):
        """مكمل للأمر hello."""
        options = self.S.listmodules() # path explotation
        
        if text:
            completions = [option for option in options if option.startswith(text)]
        else:
            completions = options
        return completions
    
    def do_workspace(self, arg):
        args = arg.split()
        if not args:
            self.print_workspace_list()
            return
        
        subcommand = args[0]
        if subcommand == "-a" or subcommand == "--add":
            if len(args) < 2:
                print("Usage: workspace -a <name>")
                return
            self.add_workspace(args[1])
        elif subcommand == "-l" or subcommand == "--list":
            self.print_workspace_list()
        elif subcommand == "-d" or subcommand == "--delete":
            if len(args) < 2:
                print("Usage: workspace -d <name>")
                return
            self.delete_workspace(args[1])
        elif subcommand == "-D" or subcommand == "--delete-all":
            self.delete_all_workspaces()
        elif subcommand == "-h" or subcommand == "--help":
            self.print_workspace_help()
        # Add more subcommands and their functionality here
        elif subcommand == "-v":
            self.print_workspace_verbose()

    def print_workspaces(self):
        print("\nWorkspaces")
        print("=" * 10 + "\n")
        print("current  name        hosts  services  vulns  creds  loots  notes")
        print("-------  ----        -----  --------  -----  -----  -----  -----")
        for workspace in self.workspaces:
            current_indicator = "*" if workspace["name"] == self.current_workspace else " "
            print(f"{current_indicator:<9} {workspace['name']:<11} {workspace['hosts']:<7} {workspace['services']:<9} {workspace['vulns']:<6} {workspace['creds']:<6} {workspace['loots']:<6} {workspace['notes']}")

    def print_workspace_verbose(self):
        print(f"\nCurrent workspace: {self.current_workspace}\n")
        print("name        hosts  services  vulns  creds  loots  notes")
        print("----        -----  --------  -----  -----  -----  -----")
        workspace = next(w for w in self.workspaces if w["name"] == self.current_workspace)
        print(f"{workspace['name']:<11} {workspace['hosts']:<7} {workspace['services']:<9} {workspace['vulns']:<6} {workspace['creds']:<6} {workspace['loots']:<6} {workspace['notes']}")

    def add_workspace(self, name):
        if name not in self.workspaces:
            self.workspaces[str(name)] = []
            print(f"Added workspace '{name}'.")
        else:
            print(f"Workspace '{name}' already exists.")

    def delete_workspace(self, name):
        if name in self.workspaces:
            del self.workspaces[name]
            print(f"Deleted workspace '{name}'.")
        else:
            print(f"Workspace '{name}' does not exist.")

    def delete_all_workspaces(self):
        self.workspaces.clear()
        print("All workspaces deleted.")

    def print_workspace_list(self):
        print("\nAvailable Workspaces:")
        for name in self.workspaces:
            print(f"  {name}")
        print("")
    def print_workspace_help(self):
        help_text = """
Usage: workspace [options]

OPTIONS:
    -a, --add <name>          Add a workspace.
    -d, --delete <name>       Delete a workspace.
    -D, --delete-all          Delete all workspaces.
    -h, --help                Help banner.
    -l, --list                List workspaces.
        """
        print(help_text)
    
    def complete_workspace(self, text, line, begidx, endidx):
        """مكمل للأمر hello."""
        options = ['default']
        # All WorkSpace .....
        if text:
            completions = [option for option in options if option.startswith(text)]
        else:
            completions = options
        return completions

    def do_set(self,args = ""):
        if args != "":
            try:
                args = args.split(" ")
                self.data[args[0]] = args[1]
                print(args[0],"=>",args[1])
            except:
                self.data[args[0]] = ""
                print(args[0],"=>","")
    
    def complete_set(self, text, line, begidx, endidx):
        """مكمل للأمر hello."""
        options = ['ConsoleLogging', 'Prompt', 'SessionTlvLogging','LogLevel','PromptChar','TimestampOutput','MeterpreterPrompt','PromptTimeFormat','MinimumRank','SessionLogging']
        # And lhosts rhosts lports rports ....etc
        if text:
            completions = [option for option in options if option.startswith(text)]
        else:
            completions = options
        return completions


    def do_setg(self,args):
        if args != "":
            try:
                args = args.split(" ")
                self.data[args[0]] = args[1]
                print(args[0],"=>",args[1])
            except:
                self.data[args[0]] = ""
                print(args[0],"=>","")

    def complete_setg(self, text, line, begidx, endidx):
        """مكمل للأمر hello."""
        options = ['world', 'friend', 'everyone']
        if text:
            completions = [option for option in options if option.startswith(text)]
        else:
            completions = options
        return completions


    def do_back(self,args):
        self.pprompt("dr>")
        self.module = None  
        self.used_module = None                
        

    def do_banner(self,args):
        sem()
        modsum = self.readDirs

        table_data = [
            ['=[ drsploit v1.0-dev ]='],
            ['+ -- --=[ {} exploits - {} auxiliary - {} post ]'.format(modsum['exploits'],modsum['auxiliary'],modsum['posts'])],
            ['+ -- --=[ {} payloads - {} encoders - {} nops  ]'.format(modsum['payloads'],modsum['encoders'],modsum['nops'])],
            ['+ -- --=[ {} evasion                         ]'.format(modsum['evasion'])]
        ]

        # إنشاء الجدول
        table = AsciiTable(table_data)

        console.print(table.table)

    def do_search(self,args):
        search_results = search_json(json_data=self.readjson,search_word=args)
        print("\nSearch ",args.capitalize(),sep="")
        print("="*len(args),end="\n\n")
        
            
        table = Table()
        table.add_column("#")
        table.add_column("Name")
        table.add_column("Disclosure Date")
        table.add_column("Rank")
        table.add_column("Check")
        table.add_column("Description")

        Dicts = self.readjson
        path: type[str] = str
        x = 0
        vs = []
        dicts = {}
        v = ""
        for var in search_results:
            for i in var['keys']:
                v += " ".join(i)
                x+=1
            console.print(dicts)

    def do_db_nmap(self,args):
        pprint()

    def do_hosts(self, arg):
        args = arg.split()
        if not args:
            self.print_hosts()
            return

    def print_hosts(self):
        print("\nHosts")
        print("=" * 10 + "\n")
        print("address  mac         name      os_name   os_flavor  os_sp  purpose  info  comments")
        print("------   ---         ----      -------   ---------  -----  -------  ----  --------")
        for host in self.hosts:
            print(f"{host['address']:<9} {host['mac']:<11} {host['name']:<9} {host['os_name']:<10} {host['os_flavor']:<12} {host['os_sp']:<6} {host['purpose']:<8} {host['info']:<6} {host['comments']}")

    def help_hosts(self):
        help_text = """
Usage: hosts [options]

Host manipulation and display.

Options:
    No additional options. Displays a list of hosts.
        """
        print(help_text)
    
    def complete_hosts(self, text, line, begidx, endidx):
        """مكمل للأمر hello."""
        options = ['-add','-columns']
        # All Hosts Options .....
        if text:
            completions = [option for option in options if option.startswith(text)]
        else:
            completions = options
        return completions

    def do_targets(self,args):
        pass
    
    def do_sessions(self, arg):
        args = arg.split()
        if not args:
            self.print_active_sessions()
            return
        
        subcommand = args[0]
        if subcommand == "-l" or subcommand == "--list":
            self.print_active_sessions()
        elif subcommand == "-i" or subcommand == "--interact":
            if len(args) < 2:
                print("Usage: sessions -i <id>")
                return
            self.interact_with_session(args[1])
        elif subcommand == "-k" or subcommand == "--kill":
            if len(args) < 2:
                print("Usage: sessions -k <id>")
                return
            self.kill_session(args[1])
        elif subcommand == "-K" or subcommand == "--kill-all":
            self.kill_all_sessions()
        elif subcommand == "-h" or subcommand == "--help":
            self.print_sessions_help()
        # Add more subcommands and their functionality here

    def interact_with_session(self, session_id):
        if session_id in self.active_sessions:
            print(f"Interacting with session {session_id}.")
        else:
            print(f"Session {session_id} is not active.")

    def kill_session(self, session_id):
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            print(f"Terminated session {session_id}.")
        else:
            print(f"Session {session_id} is not active.")

    def kill_all_sessions(self):
        self.active_sessions.clear()
        print("Terminated all sessions.")

    def print_active_sessions(self):
        print("\nActive sessions")
        print("=" * 15 + "\n")
        if not self.active_sessions:
            print("No active sessions.")
        else:
            for session_id, session_data in self.active_sessions.items():
                print(f"Session ID: {session_id}")
                print(f"Session Data: {session_data}")
                print("-" * 15)

    def print_sessions_help(self):
        help_text = """
Usage: sessions [options] or sessions [id]

Active session manipulation and interaction.

OPTIONS:
    -c, --command <command>              Run a command on the session given with -i, or all
    -C, --meterpreter-command <command>  Run a Meterpreter Command on the session given with -i, or all
    -d, --list-inactive                  List all inactive sessions
    -h, --help                           Help banner
    -i, --interact <id>                  Interact with the supplied session ID
    -k, --kill <id>                      Terminate sessions by session ID and/or range
    -K, --kill-all                       Terminate all sessions
    -l, --list                           List all active sessions
    -n, --name <id> <name>               Name or rename a session by ID
    -q, --quiet                          Quiet mode
    -s, --script <script>                Run a script or module on the session given with -i, or all
    -S, --search <filter>                Row search filter.
    -t, --timeout <seconds>              Set a response timeout (default: 15)
    -u, --upgrade <id>                   Upgrade a shell to a meterpreter session on many platforms
    -v, --list-verbose                   List all active sessions in verbose mode
    -x, --list-extended                  Show extended information in the session table

Many options allow specifying session ranges using commas and dashes.
For example:  sessions -s checkvm -i 1,3-5  or  sessions -k 1-2,5,6
        """
        print(help_text)
    def do_options(self, arg):
        args = arg.split()
        if not args:
            self.print_global_options()
            return
        
        subcommand = args[0]
        if subcommand == "-l" or subcommand == "--list":
            self.print_global_options()
        elif subcommand == "-h" or subcommand == "--help":
            self.print_global_options_help()

    def print_global_options(self):
        print("\nGlobal Options")
        print("=" * 20 + "\n")
        print("   Option             Current Setting    Description")
        print("   ------             ---------------    -----------")
        for option, value in self.global_options.items():
            print(f"   {option:<20} {value:<18} {self.get_option_description(option)}")

    def get_option_description(self, option):
        descriptions = {
            "ConsoleLogging": "Log all console input and output",
            "LogLevel": "Verbosity of logs (default 0, max 3)",
            "MeterpreterPrompt": "The meterpreter prompt string",
            "MinimumRank": "The minimum rank of exploits that will run without explicit confirmation",
            "Prompt": "The prompt string",
            "PromptChar": "The prompt character",
            "PromptTimeFormat": "Format for timestamp escapes in prompts",
            "SessionLogging": "Log all input and output for sessions",
            "SessionTlvLogging": "Log all incoming and outgoing TLV packets",
            "TimestampOutput": "Prefix all console output with a timestamp"
        }
        return descriptions.get(option, "No description available")

    def print_global_options_help(self):
        help_text = """
Usage: options [options]

Global option manipulation.

OPTIONS:
    -l, --list                List all global options
    -h, --help                Help banner
        """
        print(help_text)
    def do_services(self, arg):
        args = arg.split()
        if not args:
            self.print_services()
            return

    def print_services(self):
        print("\nServices")
        print("=" * 10 + "\n")
        print("host        port  proto  name         state     info")
        print("----        ----  -----  ----         -----     ----")
        for service in self.services:
            print(f"{service['host']:<11} {service['port']:<6} {service['proto']:<7} {service['name']:<12} {service['state']:<9} {service['info']}")

    def help_services(self):
        help_text = """
Usage: services [options]

Service manipulation and display.

Options:
    No additional options. Displays a list of services.
        """
        print(help_text)
    def do_vulns(self, arg):
        args = arg.split()
        if not args:
            self.print_vulns()
            return

    def print_vulns(self):
        print("\nVulnerabilities")
        print("=" * 15 + "\n")
        print("Timestamp          Host             Name                References")
        print("---------          ----             ----                ----------")
        for vuln in self.vulns:
            print(f"{vuln['timestamp']:<18} {vuln['host']:<16} {vuln['name']:<20} {vuln['references']}")

    def help_vulns(self):
        help_text = """
Usage: vulns [options]

Vulnerability manipulation and display.

Options:
    No additional options. Displays a list of vulnerabilities.
        """
        print(help_text)
    def do_creds(self, arg):
        args = arg.split()
        if not args:
            self.print_creds()
            return

    def print_creds(self):
        print("\nCredentials")
        print("=" * 12 + "\n")
        print("host             origin           service           public    private   realm  private_type    JtR Format")
        print("----             ------           -------           ------    -------   -----  ------------    ----------")
        for cred in self.creds:
            print(f"{cred['host']:<16} {cred['origin']:<16} {cred['service']:<18} {cred['public']:<10} {cred['private']:<10} {cred['realm']:<7} {cred['private_type']:<16}")

    def help_creds(self):
        help_text = """
Usage: creds [options]

Credential manipulation and display.

Options:
    No additional options. Displays a list of credentials.
        """
        print(help_text)
    def do_loot(self, arg):
        args = arg.split()
        if not args:
            self.print_loot()
            return

    def print_loot(self):
        print("\nLoot")
        print("=" * 4 + "\n")
        print("host  service  type  name  content  info  path")
        print("----  -------  ----  ----  -------  ----  ----")
        for item in self.loot:
            print(f"{item['host']:<6} {item['service']:<8} {item['type']:<6} {item['name']:<6} {item['content']:<9} {item['info']:<5} {item['path']:<5}")

    def help_loot(self):
        help_text = """
Usage: loot [options]

Loot manipulation and display.

Options:
    No additional options. Displays a list of loot items.
        """
        print(help_text)
    def do_notes(self, arg):
        args = arg.split()
        if not args:
            self.print_notes()
            return

    def print_notes(self):
        print("\nNotes")
        print("=" * 5 + "\n")
        print(" Time      Host      Service    Port  Protocol  Type          Data")
        print(" ----      ----      -------    ----  --------  ----          ----")
        for note in self.notes:
            print(f"{note['Time']:<11} {note['Host']:<10} {note['Service']:<10} {note['Port']:<6} {note['Protocol']:<9} {note['Type']:<13} {note['Data']:<10}")

    def help_notes(self):
        help_text = """
Usage: notes [options]

Note manipulation and display.

Options:
    No additional options. Displays a list of notes.
        """
        print(help_text)


    def do_help(self, arg):
        help_text = """
Core Commands
=============

Command       Description
-------       -----------
?             Help menu
banner        Display an awesome metasploit banner
cd            Change the current working directory
color         Toggle color
connect       Communicate with a host
debug         Display information useful for debugging
exit          Exit the console
features      Display the list of not yet released features that can be opted in to
get           Gets the value of a context-specific variable
getg          Gets the value of a global variable
grep          Grep the output of another command
help          Help menu
history       Show command history
load          Load a framework plugin
quit          Exit the console
repeat        Repeat a list of commands
route         Route traffic through a session
save          Saves the active datastores
sessions      Dump session listings and display information about sessions
set           Sets a context-specific variable to a value
setg          Sets a global variable to a value
sleep         Do nothing for the specified number of seconds
spool         Write console output into a file as well the screen
threads       View and manipulate background threads
tips          Show a list of useful productivity tips
unload        Unload a framework plugin
unset         Unsets one or more context-specific variables
unsetg        Unsets one or more global variables
version       Show the framework and console library version numbers

Module Commands
===============


Target a block from a resolved domain name:

    set RHOSTS www.example.test/24
"""
        print(help_text)

    def do_quit(self,args):
        """
        Quit the console.
        """
        print("Quit the console...")
        sys.exit()
    def do_exit(self,args):
        """
        Exit the console.
        """
        print("Exiting the console...")
        sys.exit()






def main():
    opt_parser = OptionParser(add_help_option=False)
    opt_parser.add_option("-s", "--services", dest="services", help="Start Services Sql DataBase")
    opt_parser.add_option("-u", "--update", type="str", dest="update", help="Update DrSploit")
    opt_parser.add_option("-v", "--virsun", dest="virsun", action='store_true', help="DrSploit Virsun") 
    opt_parser.add_option("-h", "--help", dest="help", action='store_true', help="Help banner") 
    opts, args = opt_parser.parse_args()

    if opts.virsun:
        console.print("DrSploit 1.0v", style="bold")
        sys.exit()
    if opts.help :
        opt_parser.print_help()
        sys.exit()
    if opts.services is None:
        services = opts.services
    if opts.update is None:
        update = opts.update
    

    S = Sort()
    with console.status("[bold]DrSploit Framework is starting ...", spinner='aesthetic') as status:
        S.woriteJsonFile()
    drs = DRConsole()
    drs.do_banner(args=None)

    while True:
        try:
            drs.cmdloop()
        except KeyboardInterrupt:
            print("Use 'exit -y' to leave")

if __name__ == "__main__":
    main()

