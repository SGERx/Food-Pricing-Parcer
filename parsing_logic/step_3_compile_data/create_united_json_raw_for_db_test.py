import glob
import json
import os
from datetime import date, datetime
import time

json_folder = '../data/c_data_clean/clean_data_json/*.json'
json_files = glob.glob(json_folder)
print(json_files)

# new_data = {}
final_data = []

for file in json_files:
    with open(file, 'r', encoding='utf-8-sig') as f:
        content = f.read()
        if len(content) > 0:
            try:
                data = json.loads(content)
                # print(data)
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                for key, values in data.items():
                    print(key)
                    print(values)
                    for value in values:
                        print(value)
                        store, category = key.split('_')
                        name = value[0]
                        price = str(value[1])
                        quantity = value[2]
                        real_price = value[3]
                        new_key = current_datetime
                        new_value = [current_datetime, store, category, name, price, quantity, real_price]
                        print(new_value)
                        final_data.append(new_value)
                        print(f"финальный список: {final_data}")
            except json.JSONDecodeError as e:
                print(f"Ошибка при чтении JSON из файла {file}: {str(e)}")
        else:
            print(f"Файл {file} пустой")

new_data_json = json.dumps(final_data, ensure_ascii=False)

output_file = f'../../data/d_data_analyse/{date.today()}_united_json_for_db.json'

with open(output_file, 'w', encoding='utf-8-sig') as outfile:
    outfile.write(new_data_json)
