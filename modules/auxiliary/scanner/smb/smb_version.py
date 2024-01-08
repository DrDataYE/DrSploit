#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import requests
from rich.console import Console
console = Console()

# محاولة استيراد impacket لفحص SMB (يتطلب تثبيت impacket)
dependencies_missing = False
try:
    from impacket.smbconnection import SMBConnection
except ImportError:
    dependencies_missing = True

# Metadata الخاصة بالأداة
metadata = {
    'name': 'SMB Version Checker',
    'description': '''
        Tool to check the SMB version of a target.
    ''',
    'authors': [
        'Your Name'
    ],
    'date': '2023-04-01',
    'license': 'YOUR_LICENSE',
    'references': [
        {'type': 'url', 'ref': 'https://www.example.com/smb-version-info'},
        {'type': 'url', 'ref': 'https://www.smb.org/'}
    ],
    'type': 'remote_exploit_cmd_stager',
    'targets': [
        {'platform': 'windows', 'arch': 'x86'},
        {'platform': 'windows', 'arch': 'x64'}
    ],
    'payload': {
        'command_stager_flavor': 'curl',
    },
    'options': {
        'targeturi': {'type': 'string', 'description': 'The base path', 'required': True, 'default': '/'},
        'rhost': {'type': 'address', 'description': 'Target address', 'required': True, 'default': None},
        'command': {'type': 'string', 'description': 'The command to execute via the q GET parameter', 'required': True}
    }
}

def check_smb_version(rhost):
    """فحص إصدار SMB للهدف المحدد."""
    try:
        conn = SMBConnection(rhost, rhost)
        smb_info = conn.get_server_os_info()
        return {
            'name': smb_info[0],
            'version': smb_info[1]
        }
    except Exception as e:
        console.print(f"[bold red][-] [white not bold]Error during SMB check: {e}")
        return None

def run(args):
    if dependencies_missing:
        console.print('[bold red][-] [white not bold]Module dependency (impacket) is missing, cannot continue')
        return

    smb_info = check_smb_version(args['rhost'])
    if smb_info:
        console.print(f"[bold green][+] [white not bold]SMB Name: {smb_info['name']}, Version: {smb_info['version']}")
    else:
        console.print("[bold red][-] [white not bold]Unable to retrieve SMB information.")

