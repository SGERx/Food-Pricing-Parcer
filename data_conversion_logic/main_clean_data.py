from data_conversion_logic.main_clean_output_data import jsonify_data, write_to_csv


def main_clean_data(name):
    json_data = jsonify_data(name)
    write_to_csv(name, json_data)
    print(f"очистка и запись данных по {name} завершена в JSON и CSV")
