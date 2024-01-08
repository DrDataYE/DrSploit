#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import ftplib
from rich.console import Console
console = Console()

# Metadata الخاصة بأداة فحص FTP
metadata = {
    'name': 'FTP Version Checker',
    'description': 'Tool to check the FTP version of a target.',
    'authors': ['DrDataYE'],
    'date': '2023-04-01',
    'license': 'YOUR_LICENSE',
    'references': [
        {'type': 'url', 'ref': 'https://www.example.com/ftp-info'},
    ],
    'options': {
        'rhost': {'type': 'address', 'description': 'Target address', 'required': True, 'default': None},
        'ftp_port': {'type': 'int', 'description': 'FTP port', 'required': False, 'default': 21}
    }
}

def check_ftp_version(rhost, port):
    """فحص إصدار FTP للهدف المحدد."""
    try:
        with ftplib.FTP() as ftp:
            ftp.connect(rhost, port)
            ftp.login()  # يمكن تعديل هذا إذا كانت هناك حاجة لبيانات اعتماد خاصة
            return ftp.getwelcome()
    except Exception as e:
        console.print(f"[bold red][-] [white not bold]Error during FTP check: {e}")
        return None

def run(args):
    rhost = args.get('rhost')
    ftp_port = args.get('ftp_port', 21)
    console.print("[bold blue][+] [white not bold]Start Scan FTP version in",args['rhost'])
    ftp_info = check_ftp_version(rhost, ftp_port)
    if ftp_info:
        console.print(f"[bold green][+] [white not bold]FTP Banner: {ftp_info}")
    else:
        console.print("[bold red][-] [white not bold]Unable to retrieve FTP information.")

