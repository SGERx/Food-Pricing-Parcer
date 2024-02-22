import glob
import json
import os
import shutil
from datetime import date, datetime


def create_json():
    json_folder = '../data/c_data_clean/clean_data_json/*.json'
    json_files = glob.glob(json_folder)
    print(json_files)

    final_data = []

    for file in json_files:
        with open(file, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            if len(content) > 0:
                try:
                    data = json.loads(content)

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

    output_file = f'../data/d_data_analyse/{date.today()}_united_json_for_db.json'

    with open(output_file, 'w', encoding='utf-8-sig') as outfile:
        outfile.write(new_data_json)

    source_dir = f"../data/c_data_clean/clean_data_json/"
    target_dir = f"../data/c_data_clean/archived_json/"

    file_names = os.listdir(source_dir)

    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)


if __name__ == '__main__':
    create_json()
