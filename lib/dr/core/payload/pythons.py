import base64
import zlib

def create_exec_stub(cmd):
    """
    Encode the given python command in base64 and wrap it with a stub
    that will decode and execute it on the fly. The code will be condensed to
    one line and compatible with all Python versions supported by the Python
    Meterpreter stage.

    :param cmd: The python code to execute.
    :return: Full python stub to execute the command.
    """
    # Compress and then encode the command
    payload = base64.b64encode(zlib.compress(cmd.encode())).decode()

    # Create the Python stub for decoding and executing
    b64_stub = f"exec(__import__('zlib').decompress(__import__('base64').b64decode(__import__('codecs').getencoder('utf-8')('{payload}')[0])))"
    
    return b64_stub

# Example usage
cmd = "print('Hello, World!')"
stub = create_exec_stub(cmd)
print(stub)
