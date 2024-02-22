from parsing_logic.parse_all import parse_all

url = "https://www.perekrestok.ru"
searchbar_xpath = "//input[@class='Input__InputStyled-sc-1kqlv3u-0 caFtVc']"
main_page_button_xpath = "//a[@href='/']"
clear_button_xpath = "//button[@class='sc-eCstlR jeYPke search-form__button search-form__button-clear']"
prodcards_xpath = "//a[@class='product-card__link']"
title_xpath = "//h1[@class='sc-fubCzh ibFUIH product__title']"
price_xpath = "//div[@class='price-card-unit-value']"
csv_name = "perekrestok"
error_text = "FLASK_PEREKRESTOK ERROR"

def flask_perekrestok():
    parse_all(url, searchbar_xpath, main_page_button_xpath, clear_button_xpath, prodcards_xpath, title_xpath,
              price_xpath, csv_name, error_text)


if __name__ == '__main__':
    flask_perekrestok()
