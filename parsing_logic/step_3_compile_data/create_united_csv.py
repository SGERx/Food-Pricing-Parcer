import os
import csv
from datetime import date

folder = f"../data/c_data_clean/clean_data_csv/"

today = date.today()

files = os.listdir(folder)

csv_files = [file for file in files if file.startswith(str(today))]

if len(csv_files) == 0:
    print('Нет файлов за сегодняшнюю дату!')

output_file = f'../data/d_data_analyse/{today}_united_csv.csv'

if not os.path.exists(output_file):
    open(output_file, "w").close()
with open(output_file, 'w', newline='', encoding='utf-8-sig') as outfile:
    writer = csv.writer(outfile)
    for file in csv_files:
        file_path = os.path.join(folder, file)
        with open(file_path, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)

            writer.writerow(['Лист ' + file])
            writer.writerow([])

            for row in reader:
                writer.writerow(row)
                writer.writerow([])
