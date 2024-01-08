import uuid
import binascii
import socket

class SendUUID:
    def __init__(self, sock=None):
        self.sock = sock if sock is not None else socket.socket()

    def generate_uuid(self):
        # توليد UUID
        return uuid.uuid4()

    def send_uuid(self, uuid_value=None):
        if uuid_value is None:
            uuid_value = self.generate_uuid()

        # تحويل UUID إلى تمثيل سداسي عشري
        uuid_hex = uuid_value.hex

        # إرسال UUID عبر الsocket
        self.sock.send(binascii.a2b_hex(uuid_hex))

# استخدام الكلاس
if __name__ == "__main__":
    # يمكنك هنا تحديد الsocket أو استخدام الsocket الافتراضي
    sender = SendUUID()
    sender.send_uuid()
