from data_conversion_logic.main_clean_data import main_clean_data

name = "miratorg"


def flask_clean_data_miratorg():
    main_clean_data(name)


if __name__ == '__main__':
    main_clean_data(name)
