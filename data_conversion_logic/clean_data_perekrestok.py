from data_conversion_logic.main_clean_data import main_clean_data

name = "perekrestok"


def flask_clean_data_perekrestok():
    main_clean_data(name)


if __name__ == '__main__':
    main_clean_data(name)
