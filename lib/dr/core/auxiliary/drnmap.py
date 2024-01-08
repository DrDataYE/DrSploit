#!/bin/python3

import sys
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import track
from rich.console import Console
import nmap
from nmap import PortScanner,PortScannerError









console = Console()


msg_help = """# DrScan 1.0 ( https://www.cyber1101.com )

Usage: 
    drscan [Scan Type(s)] [Nmap Options] {target specification} 

Example:
    drscan -sV 192.168.0.1/24
    drscan -v -A --subdomains www.cyber1101.com

SEE THE MAN PAGE ( https://www.cyber1101.com/man.html ) FOR MORE OPTIONS AND EXAMPLES
"""


# lport = None
def drnmap(targets="127.0.0.1",port="1-21",arg=""):
        try:
            import sys
            # Scann Ports
            nm = PortScanner()
            try:
                nm.scan(ports=port,hosts=targets,arguments=arg,timeout=0)
            except PortScannerError as e:
                print(((str('%s'%(e)).replace("'","")).replace("nmap","drscan")).replace(r"\r\n",r"\n"))
                sys.exit()
                # console.print("\n",e,style="red")
            result = []
            # lport = ()
            for host in nm.all_hosts():
                result.append(nm[host])
                
                for proto in nm[host].all_protocols():
                    lport = nm[host][proto].keys()
            return result, lport
        except:
            pass


def pprint(arg,listport) -> None:
    for numbs in range(len(arg)):
        args = arg[numbs]
        MARKDOWN = "# DrScan %i"% (numbs)
        md = Markdown(MARKDOWN)
        console.print(md)
        for adas in ['addresses']: # status
            console.print(adas.capitalize(),style="bold green")
            for column in args[adas]:
                console.print("\t",column + ":",args[adas][column])
        # console.print("[bold green]Vendor",args['vendor'],sep="\t")
        
        for title in args:  
            if 'tcp' == title or 'udp' == title:
                scripts = []
                table = Table(title="Ports %s"% (title))
                for i in ['port','state','name','product','version']:
                    table.add_column(i.capitalize())
                
                
                for i in listport:
                    try:
                        table.add_row(str(i), args[title][i]['state'],args[title][i]['name'], args[title][i]['product'],args[title][i]['version'],style="green")
    
                        try:
                            # print("Protocol :",i,hii['tcp'][i]['script'])
                            for j in args[title][i]['script']:
                                scripts.append("[bold underline white on green] {}/{}:  {} {}".format(title,i,j,"[/]"))
                                scripts.append(args[title][i]['script'][j])
                        except:
                            pass
                            
                    except:
                        pass
                console.print(table,"\n\n")
                console.print('\n'.join(scripts))
            elif 'osmatch' == title:
                try:
                    console.print("System Information",style="bold green",justify='center')
                    console.print("\t[bold green]OS Name :",args['osmatch'][0]['name'])
                    console.print("\t[bold green]OS Family :",args['osmatch'][0]['osclass'][0]['osfamily'])
                    console.print("\t[bold green]Vendor :",args['osmatch'][0]['osclass'][0]['vendor'])
                    console.print("\t[bold green]OS Gen :",args['osmatch'][0]['osclass'][0]['osgen'])
                    console.print("\t[bold green]Accuracy :",args['osmatch'][0]['osclass'][0]['accuracy'])
                    console.print("\t[bold green]Cpe :",args['osmatch'][0]['osclass'][0]['cpe'][0])

                except:
                    console.print("[bold green]OS Name :","[red]Uknown")
            elif 'hostscript' in title:
                console.print("\n\n",'hostscript'.capitalize(),style='bold green',justify="center")
                for i in range(len(args['hostscript'])):
                    console.print(args['hostscript'][i]['id'],style='bold green')
                    console.print("\t",args['hostscript'][i]['output'])
             
                
                # msg = Table.grid(padding=1, )
                # msg.add_column(style="green",justify='right',)
                # msg.add_column(no_wrap=True)
                # msg.add_row("hhh","hhhhhhhhhhhhhhhhhhhh")
                # msg.add_row("sdcvgsdvhsd","sdujgsduygscuydgu")
                # console.print(msg)



     









    
