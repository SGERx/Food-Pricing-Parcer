from parsing_logic.main_parsing_logic import input_parsing, open_page, product_cards_parcing, write_to_csv, driver


def parse_all(url, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath, title_xpath, price_xpath, csv_name, error_text):
    try:
        with driver:
            product_list = input_parsing()
            print(product_list)
            open_page(url)
            print('Сейчас будем парсить')
            full_dict = product_cards_parcing(product_list, searchbar_xpath, main_page_button_xpath, clear_button_xpath,
                                              prodcards_xpath, title_xpath, price_xpath)
            write_to_csv(full_dict, csv_name)
            print(f"Конец теста")
    except:
        print(error_text)



