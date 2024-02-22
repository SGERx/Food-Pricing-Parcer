from data_conversion_logic.main_clean_data import main_clean_data

name = "auchan"


def flask_clean_data_auchan():
    main_clean_data(name)


if __name__ == '__main__':
    main_clean_data(name)
