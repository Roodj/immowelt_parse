from bs4 import BeautifulSoup
import requests

URL = "https://www.immowelt.de/classified-search?distributionTypes=Rent&estateTypes=House,Apartment&locations=AD08DE6863&priceMax=800"

def parse_resault():
    houses_desc_list = []
    response = requests.get(URL).text
    soup = BeautifulSoup(response, 'lxml')
    soup_general = soup.find(class_='css-183toqv') # div с целевым городом
    soup_additional = soup.find(class_='css-1pq2iqw') # div с городами рядом
    soup_cards = soup_general.find_all(class_='css-79elbk')
    
    for card in soup_cards:
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
if __name__ == '__main__':
    print(parse_resault())