from data_conversion_logic.main_clean_data import main_clean_data

name = "metro"


def flask_clean_data_metro():
    main_clean_data(name)


if __name__ == '__main__':
    main_clean_data(name)
