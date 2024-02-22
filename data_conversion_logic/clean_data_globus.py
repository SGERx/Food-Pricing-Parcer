from data_conversion_logic.main_clean_data import main_clean_data

name = "globus"


def flask_clean_data_globus():
    main_clean_data(name)


if __name__ == '__main__':
    main_clean_data(name)
