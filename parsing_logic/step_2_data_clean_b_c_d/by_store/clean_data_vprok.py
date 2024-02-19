from parsing_logic.step_2_data_clean_b_c_d.clean_data_logic_price import jsonify_data, write_to_csv


name = "vprok"

if __name__ == '__main__':
    json_data = jsonify_data(name)
    write_to_csv(name, json_data)
    print("очистка и запись данных по vprok завершена в JSON и CSV")
