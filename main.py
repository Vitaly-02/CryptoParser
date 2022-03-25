import os
import requests
from bs4 import BeautifulSoup


def update_info(base):
    url = 'https://coinmarketcap.com'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    names = soup.find_all(class_='sc-1eb5slv-0 iworPT')
    prices = soup.find_all(class_='sc-131di3y-0 cLgOOr')
    market_caps = soup.find_all(class_="sc-1ow4cwt-1 ieFnWP")

    for i in range(0, len(names) - 9):
        currency = {i: {'name': names[i + 9].get_text(), 'market_cap': market_caps[i].get_text(),
                        'price_usd': prices[i + 3].get_text()}}
        base.update(currency)


def print_info(base):
    print('Name                  Market capitalization        Price')
    for item in base:
        print('{0:21} {1:28} {2:21}'.format(base[item]['name'], base[item]['market_cap'], base[item]['price_usd']))


def find_by_name(name, base):
    # sorting
    sorted_base = sorted(base.items(), key=lambda x: x[1]['name'])
    # binary search
    start = 0
    end = len(sorted_base) - 1
    mid = int(end / 2)
    index = -1
    while start < mid < end:
        if sorted_base[mid][1]['name'] == name:
            index = mid
            break
        elif sorted_base[mid][1]['name'] > name:
            end = mid
            mid = int(end / 2)
        else:
            start = mid
            mid = int((end - start) / 2) + start
    if index == -1:
        print("Can't find {0}".format(name))
    else:
        print('{0:21} {1:28} {2:21}'.format(sorted_base[index][1]['name'], sorted_base[index][1]['market_cap'],
                                            sorted_base[index][1]['price_usd']))


if __name__ == '__main__':
    base1 = {}
    update_info(base1)

    key = input('Enter P to print info, U to update info, F to find by name, Q to quit\nInput: ')
    while key != 'Q':

        if key == 'P':
            os.system('cls' if os.name == 'nt' else 'clear')
            print_info(base1)
        elif key == 'U':
            update_info(base1)
            os.system('cls' if os.name == 'nt' else 'clear')
            print_info(base1)
        elif key == 'F':
            name_to_find = input('Enter cryptocurrency name to get info\nInput: ')
            find_by_name(name_to_find, base1)

        key = input('Enter P to print info, U to update info, F to find by name, Q to quit\nInput: ')