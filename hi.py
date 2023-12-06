
# from schema import Schema

# schema = Schema([{'name': str,
#                  'city': str, 
#                  'closeness (1-5)': int,
#                  'extrovert': bool,
#                  'favorite_temperature': float}])
                 
# schema.validate(data)
# print(schema.__dict__)


file_path = r'C:\Users\Dr Data\Desktop\drsploit\modules\auxiliary\scanner\example.py'

# try:
#     module = __import__(file_path[:-3])
#     if hasattr(module, 'metadata'):
#         metadata_var = getattr(module, 'metadata')
#         # قم بمعالجة المتغير هنا
#         print(metadata_var)
#     else:
#         print("المتغير metadata غير معرف في الملف")
# except ImportError:
#     print("يتعذر استيراد الملف")

# file_path = '/path/to/file.py'

import pyfiglet

# تحديد نص Metasploit
text = "DrSploit"

# إنشاء بانر Metasploit
banner = pyfiglet.figlet_format(text)

# طباعة البانر
print(banner)

import json

