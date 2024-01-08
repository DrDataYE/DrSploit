#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import ftplib
import threading
from queue import Queue
from rich.console import Console

console = Console()
print_lock = threading.Lock()


# Metadata الخاصة بأداة فحص FTP وتسجيل الدخول
metadata = {
    'name': 'FTP Login Checker',
    'description': 'Tool to check FTP login on a target.',
    'authors': ['Your Name'],
    'date': '2023-04-01',
    'license': 'YOUR_LICENSE',
    'references': [
        {'type': 'url', 'ref': 'https://www.example.com/ftp-info'},
    ],
    'options': {
        'rhost': {'type': 'address', 'description': 'Target address', 'required': True, 'default': None},
        'ftp_port': {'type': 'int', 'description': 'FTP port', 'required': False, 'default': 21},
        'username_file': {'type': 'string', 'description': 'Path to file with list of usernames', 'required': False, 'default': None},
        'password_file': {'type': 'string', 'description': 'Path to file with list of passwords', 'required': False, 'default': None},
        'threads': {'type': 'int', 'description': 'Number of threads', 'required': False, 'default': 5}
    }
}

def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]
def ftp_login_test(rhost, port, username, password, results, print_lock):
    try:
        with ftplib.FTP() as ftp:
            ftp.connect(rhost, port)
            ftp.login(username, password)
            results.put((username, password, True))
            with print_lock:
                console.print(f"[bold green][+] [white not bold]Login successful: {username}/{password}")
    except ftplib.error_perm:
        results.put((username, password, False))
        with print_lock:
            console.print(f"[bold red][-] [white not bold]Login failed: {username}/{password}")
    except Exception as e:
        with print_lock:
            console.print(f"[bold red][-] [white not bold]Error during login attempt: {e}")
        results.put((username, password, False))

def threaded_ftp_login(rhost, port, usernames, passwords, thread_count, print_lock):
    threads = []
    results = Queue()

    for username in usernames:
        for password in passwords:
            t = threading.Thread(target=ftp_login_test, args=(rhost, port, username, password, results, print_lock))
            t.start()
            threads.append(t)
            # Ensure not to exceed the thread count
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
    rhost = args.get('rhost')
    ftp_port = args.get('ftp_port', 21)
    thread_count = args.get('threads', 5)
    usernames = read_file(args['username_file']) if args.get('username_file') else []
    passwords = read_file(args['password_file']) if args.get('password_file') else []

    console.print("[bold blue][+] [white not bold]Start Login FTP in",args['rhost'])
    threaded_ftp_login(rhost, ftp_port, usernames, passwords, thread_count, print_lock)
