import os
import sys
import argparse
from gpt4zero import AI_Client

# Инициализация клиента ИИ
client = AI_Client()

# Поддерживаемые расширения файлов
supported_extensions = {'.txt', '.md', '.csv', '.json', '.xml', '.html', '.yml', '.yaml', '.ini', '.cfg', '.log'}

# Настройка аргументов командной строки
parser = argparse.ArgumentParser(description='Переименовывает файлы на основе их содержимого.')
parser.add_argument('directory', type=str, nargs='?', default='.', help='Директория для обработки файлов (по умолчанию текущая)')
args = parser.parse_args()

# Проверка существования директории
directory = args.directory
if not os.path.isdir(directory):
   print(f"Ошибка: {directory} не существует или не является директорией.")
   sys.exit(1)

# Получение списка файлов в указанной директории
files = []
for f in os.listdir(directory):
   file_path = os.path.join(directory, f)
   if os.path.isfile(file_path) and os.path.splitext(f)[1].lower() in supported_extensions:
       files.append(file_path)

# Обработка каждого файла
for file in files:
   # Чтение содержимого файла
   with open(file, 'r', encoding='utf-8') as f:
       content = f.read()

   # Формирование запроса
   messages = [{
       "role": "user", 
       "content": f"""
       Переименуй файл на основе следующего содержимого:
       ```
       {content}
       ```
       Напиши 1 название и все, без какого-либо еще текста (но пиши расширение файла). 
       Не используй пробелы и подобные знаки, для разделения можешь использовать - или _.
       Можешь писать названия на кириллице (если  например внутри текст на русском языке, вообще не обязательно называть кириллицей - если ты сам захочешь). 
       Если файл переименовывать не надо, то напиши такое же название что и было
       """
   }]

   # Отправка запроса
   while True:
    try:
        response = client.chat(messages)
        new_file_name = response.strip() 
        break
    except Exception as e:
        pass

   # Получение нового имени файла из ответа
   new_file_name = response

   # Проверка, что новое имя не пустое и отличается от старого
   if new_file_name and new_file_name != os.path.basename(file):
       # Переименование файла
       new_file_path = os.path.join(directory, new_file_name)
       os.rename(file, new_file_path)
       print(f"Файл '{file}' переименован в '{new_file_path}'")
   else:
       print(f"Файл '{file}' не был переименован (новое имя пустое или совпадает с текущим).")
