import json
import argparse
from rich.console import Console
from rich.table import Table
from rich import box

# إضافة مسار إلى sys.path لاستيراد config من المجلد الفرعي
import sys
sys.path.append('config')

#import config
from config import config

# إعداد argparse لتحليل الأوامر البرمجية
parser = argparse.ArgumentParser(description="DrSploit Information Display")
parser.add_argument("-l", "--language", help="Set the language for display", default=config.DEFAULT_LANGUAGE)
args = parser.parse_args()

# تحميل البيانات من ملف JSON
with open('languages.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# استخدام اللغة المحددة من argparse أو الافتراضية من config.py
language = args.language

# التحقق من وجود اللغة في البيانات
if language not in data:
    raise ValueError(f"Language '{language}' not found in the data.")

info = data[language]

# إنشاء كائن Console
console = Console()

# إنشاء جدول لعرض المعلومات
table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
table.add_column("Feature", justify="right")
table.add_column("Value", justify="left")

# إضافة البيانات إلى الجدول
for key, value in info.items():
    table.add_row(key, value)

# عرض الجدول
console.print(table)

