import os
import random
def convert_metasploit_color_codes(text):
    text = text.replace("%clr", "\033[0m")   # Reset color
    text = text.replace("%bld", "\033[1m")   # Bold text
    text = text.replace("%grn", "\033[32m")  # Green text
    text = text.replace("%yel", "\033[33m")  # Yellow text
    text = text.replace("%red", "\033[31m")  # Red text
    text = text.replace("%blu", "\033[34m")  # Blue text
    text = text.replace("%cyn", "\033[36m")  # Cyan text
    text = text.replace("%mag", "\033[35m")  # Magenta text
    text = text.replace("%whi", "\033[37m")  # White text
    text = text.replace("%blk", "\033[30m")  # Black text
    text = text.replace("%cya", "\033[36m")  # Cyan text (alternative)
    text = text.replace("%dred", "\033[31;2m") # Dark Red text
    return text

def print_random_file_content(folder_path):
    try:
        # قائمة بجميع الملفات في المجلد
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        # اختيار ملف عشوائي
        random_file = random.choice(files)
        file_path = os.path.join(folder_path, random_file)

        # طباعة اسم الملف المختار
        print(f"Selected file: {random_file}")

        # فتح الملف وطباعة محتواه
        with open(file_path, 'r') as file:
            print(convert_metasploit_color_codes(file.read()))

    except IndexError:
        print("The folder is empty.")
    except FileNotFoundError:
        print("Folder not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
def sem(args=None):
	# استخدم الدالة مع مسار المجلد الذي تريد فحصه
	print_random_file_content("./data/logos")

#sem_10()