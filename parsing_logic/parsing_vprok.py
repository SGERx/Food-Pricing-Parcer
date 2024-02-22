from parsing_logic.parse_all import parse_all

url = "https://www.vprok.ru"
searchbar_xpath = "//input[@class='Input_input__couZC']"
main_page_button_xpath = "//a[@href='/']"
clear_button_xpath = "//svg[@class='Input_clear__iom_A']"
prodcards_xpath = "//article[contains(@class, MainProductTile_root)]/child::a"
title_xpath = "//h1[contains(@class, Title_title__)]"
price_xpath = "//span[contains(@class, 'Price_price__')]"
csv_name = "vprok"
error_text = "FLASK_VPROK ERROR"


def flask_vprok():
    parse_all(url, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath, title_xpath,
              price_xpath, csv_name, error_text)


if __name__ == '__main__':
    flask_vprok()
