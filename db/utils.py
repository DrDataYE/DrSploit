# # # import json


# # # def search_json(file_path, search_word):
# # #     with open(file_path, 'r') as file:
# # #         json_data = json.load(file)
# # #         if isinstance(json_data, dict):
# # #             search_dict(json_data, search_word.lower())

# # # def search_dict(data, search_word, parent_keys=[]):
# # #     for key, value in data.items():
# # #         current_keys = parent_keys + [key]
# # #         if isinstance(value, dict):
# # #             search_dict(value, search_word, current_keys)
# # #         elif isinstance(value, list):
# # #             search_list(value, search_word, current_keys)
# # #         elif isinstance(value, str) and search_word in value.lower():
# # #             print(f"تم العثور على '{search_word}' في قيمة مفتاح '{'.'.join(current_keys)}': {value}")

# # # def search_list(data_list, search_word, parent_keys=[]):
# # #     for index, item in enumerate(data_list):
# # #         current_keys = parent_keys + [str(index)]
# # #         if isinstance(item, dict):
# # #             search_dict(item, search_word, current_keys)
# # #         elif isinstance(item, list):
# # #             search_list(item, search_word, current_keys)
# # #         elif isinstance(item, str) and search_word in item.lower():
# # #             print(f"تم العثور على '{search_word}' في القائمة الموجودة في مفتاح '{'.'.join(parent_keys)}', العنصر رقم {index}: {item}")

# # # # استخدام الوظيفة
# # # file_path = "./db/modules_drdata_base.json"
# # # search_word = "get"
# # # search_json(file_path, search_word)

# # from rich import print
# # from rich.table import Table
# # from rich.console import Console

# # import json

# # def search_json(file_path, search_word):
# #     with open(file_path, 'r') as file:
# #         json_data = json.load(file)
# #         if isinstance(json_data, dict):
# #             search_dict(json_data, search_word.lower())

# # def search_dict(data, search_word, parent_keys=[]):
# #     for key, value in data.items():
# #         current_keys = parent_keys + [key]
# #         if isinstance(value, dict):
# #             search_dict(value, search_word, current_keys)
# #         elif isinstance(value, list):
# #             search_list(value, search_word, current_keys)
# #         elif isinstance(value, str) and search_word in value.lower():
# #             print_search_result(current_keys, value, search_word)

# # def search_list(data_list, search_word, parent_keys=[]):
# #     for index, item in enumerate(data_list):
# #         current_keys = parent_keys + [str(index)]
# #         if isinstance(item, dict):
# #             search_dict(item, search_word, current_keys)
# #         elif isinstance(item, list):
# #             search_list(item, search_word, current_keys)
# #         elif isinstance(item, str) and search_word in item.lower():
# #             print_search_result(current_keys, item, search_word)

# # def print_search_result(keys, value, search_word):
# #     console = Console()
# #     table = Table(show_header=True, header_style="bold magenta")
# #     table.add_column("Key")
# #     table.add_column("Value")
    
# #     key_path = '.'.join(keys)
    
# #     if search_word in value.lower():
# #         highlighted_value = value.lower().replace(search_word.lower(), f"[bold yellow]{search_word.lower()}[/bold yellow]")
# #         table.add_row(key_path, highlighted_value)
# #     else:
# #         table.add_row(key_path, value)
    
# #     console.print(table)

# # # استخدام الوظيفة
# # file_path = "./db/modules_drdata_base.json"
# # search_word = "python"
# # search_json(file_path, search_word)

# from rich import print
# from rich.table import Table

# import json

# def search_json(json_data, search_word):
#         if isinstance(json_data, dict):
#             search_dict(json_data, search_word.lower())
            
            

# def search_dict(data, search_word, parent_keys=[]):
#     for key, value in data.items():
#         current_keys = parent_keys + [key]
#         if isinstance(value, dict):
#             search_dict(value, search_word, current_keys)
#         elif isinstance(value, list):
#             search_list(value, search_word, current_keys)
#         elif isinstance(value, str) and search_word in value.lower():
#             print((current_keys, value, search_word))
            
#     # return lists
#             print_search_result(current_keys, value, search_word)

# def search_list(data_list, search_word, parent_keys=[]):
#     for index, item in enumerate(data_list):
#         current_keys = parent_keys + [str(index)]
#         if isinstance(item, dict):
#             search_dict(item, search_word, current_keys)
#         elif isinstance(item, list):
#             search_list(item, search_word, current_keys)
#         elif isinstance(item, str) and search_word in item.lower():
#             print(current_keys,item,search_word)
#             print_search_result(current_keys, item, search_word)

# def print_search_result(keys, value, search_word):
#     table = Table(show_header=True, header_style="bold magenta")
#     table.add_column("Key")
#     table.add_column("Value")
    
#     key_path = '.'.join(keys)
    
#     if search_word in value.lower():
#         highlighted_value = value.lower().replace(search_word.lower(), f"[bold yellow]{search_word.lower()}[/bold yellow]")
#         table.add_row(key_path, highlighted_value)
#     else:
#         table.add_row(key_path, value)
    
#     print(table)

# # استخدام الوظيفة
# file_path = "./db/modules_drdata_base.json"
# search_word = "python"
# search_json(file_path, search_word)

import json
from rich import print

def search_json(json_data, search_word):
    results = []
    
    if isinstance(json_data, dict):
        search_dict(json_data, search_word.lower(), results)

    return results

def search_dict(data, search_word, results, parent_keys=[]):
    for key, value in data.items():
        current_keys = parent_keys + [key]
        if isinstance(value, dict):
            search_dict(value, search_word, results, current_keys)
        elif isinstance(value, list):
            search_list(value, search_word, results, current_keys)
        elif isinstance(value, str) and search_word in value.lower():
            results.append({
                'keys': current_keys,
                'value': value,
                'search_word': search_word
            })

def search_list(data_list, search_word, results, parent_keys=[]):
    for index, item in enumerate(data_list):
        current_keys = parent_keys + [str(index)]
        if isinstance(item, dict):
            search_dict(item, search_word, results, current_keys)
        elif isinstance(item, list):
            search_list(item, search_word, results, current_keys)
        elif isinstance(item, str) and search_word in item.lower():
            results.append({
                'keys': current_keys,
                'value': item,
                'search_word': search_word
            })

# استخدام الوظيفة
# file_path = "./db/modules_drdata_base.json"
# with open(file_path) as f:
#     json_data = json.load(f)
# search_word = "python"
# search_results = search_json(json_data, search_word)

# طباعة نتائج البحث
# print(search_results[0]['keys'][0])
# for i in search_results:
#     print(i)
# for result in search_results:
#     print(f"Key: {'.'.join(result['keys'])}")
#     print(f"Value: {result['value']}")
#     print(f"Search Word: {result['search_word']}")
#     print()