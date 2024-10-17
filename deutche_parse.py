import requests_cache
from bs4 import BeautifulSoup
from urllib.parse import urljoin

MAIN_PAGE_URL = "https://www.immowelt.de/classified-search?distributionTypes=Rent&estateTypes=House"

def link_gen(location='AD08DE6863', price='800'):
    """зачатки генератора ссылок"""
    ap_location = "Apartment&locations=" + location
    ap_max_price = "priceMax=" + price
    return f'{MAIN_PAGE_URL},{ap_location}&{ap_max_price}'

def parse_main():
    # TODO: docstring
    houses_desc_list = []
    session = requests_cache.CachedSession()
    response = session.get(link_gen()).text
    soup = BeautifulSoup(response, 'lxml')
    soup_general = soup.find(class_='css-183toqv') # div с целевым городом
    # soup_additional = soup.find(class_='css-1pq2iqw') # div с городами рядом
    soup_cards = soup_general.find_all(class_='css-79elbk')
    
    for card in soup_cards:
        # TODO :enumerate
        card_dict = {}

        prop_general = card.find(class_='css-xt08q3')
        prop_link = prop_general['href']
        prop_data_list = prop_general['title'].split('-')
        prop_address = card.find(class_='css-ymsudv').text

        card_dict['link'] = prop_link
        card_dict['type'] = prop_data_list[0]
        card_dict['city'] = prop_data_list[1]
        card_dict['price'] = prop_data_list[2]
        card_dict['char'] = prop_data_list[3]
        card_dict['address'] = prop_address

        houses_desc_list.append(card_dict)
    return houses_desc_list

def parse_card(link):
    '''
    Парсит страницу с объявлением по ссылке и возвращает словарь:
    {
        'link': '',
        'full_price': '', 
        'bail': '', 
        'rooms': '', 
        'livin_space': '', 
        'date_in': '', 
        'address': '',
        }
    '''
    houses_desc_list = {}
    session = requests_cache.CachedSession()
    response = session.get(link).text
    soup = BeautifulSoup(response, 'lxml')

    full_price = soup.find('div', attrs={'class':'css-47miec'})
    bail = soup.find('div', attrs={'class':'css-yxuej5'})

    chars_div = soup.find('div', attrs={'class':'css-jtsp8r'})
    chars_span = chars_div.find_all('span', attrs={'class':'css-2bd70b'})
    rooms = chars_span[0]
    livin_space = chars_span[1]
    date_in = chars_span[2]

    address = soup.find('div', attrs={'class':'css-ompuv2'})
    # contacts = soup.find_all('button', attrs={'class':'css-8g1nzq'})
    
    # TODO: блок с описанием
    # TODO: разобраться с контактами

    houses_desc_list['link'] = link
    houses_desc_list['full_price'] = full_price.text
    houses_desc_list['bail'] = bail.text
    houses_desc_list['rooms'] = rooms.get_text()
    houses_desc_list['livin_space'] = livin_space.get_text()
    houses_desc_list['date_in'] = date_in.get_text()
    houses_desc_list['address'] = address.text
    # houses_desc_list['contacts'] = contacts

    return houses_desc_list

    
if __name__ == '__main__':
    print(parse_main())
    print('----' * 10)
    print(parse_card('https://www.immowelt.de/expose/f344c6d4-1aac-4750-9e73-2fa04c151d55?ln=classified_search_results&search=distributionTypes%3DRent%26estateTypes%3DHouse%2CApartment%26locations%3DAD08DE6863%26priceMax%3D800&m=classified_search_results_classified_classified_detail'))