import os
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


def update_info(base):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    parameters = {
        'start': '1',
        'limit': '25',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'your_api_key',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        results = response.json()
        data = results['data']
        for currency in data:
            info = {currency['id']: {'name': currency['name'], 'market_cap': currency['quote']['USD']['market_cap'],
                                     'price_usd': currency['quote']['USD']['price']}}
            base.update(info)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    print_info(base)


def print_info(base):
    print('Name                  Market capitalization        Price')
    for item in base:
        print(f"{base[item]['name']:15} {base[item]['market_cap']:28} {base[item]['price_usd']:21}")


def find_by_name(name, base):
    # sorting
    sorted_base = sorted(base.items(), key=lambda x: x[1]['name'])
    # binary search
    start = 0
    end = len(sorted_base) - 1
    mid = int(end / 2)
    index = -1
    while start <= 9 and end >= 0:
        if sorted_base[mid][1]['name'] == name:
            index = mid
            break
        elif sorted_base[mid][1]['name'] > name:
            end = mid - 1
            mid = int((start + end) / 2)
        else:
            start = mid + 1
            mid = int((start + end) / 2)
    if index == -1:
        print(f"Can't find {name}")
    else:
        print(f"{sorted_base[index][1]['name']:21} {sorted_base[index][1]['market_cap']:28} "
              f"{sorted_base[index][1]['price_usd']:21}")


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
