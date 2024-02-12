import argparse
import requests
from urllib import parse

import bs4
from opencc import OpenCC


def _parse_response(response: requests.Response) -> list[str]:
    """
    Parse the response using BeautifulSoup and return a list of strings from the first column.

    Args:
        response (requests.Response): The response object to be parsed.

    Returns:
        list[str]: A list of strings from the first column.
    """
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', border="1")
    first_column_content = []
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 0:
            first_column_content.append(cells[0].text)
    return first_column_content

def get_jyutping_multiple(character):
    assert len(character) == 1 and '\u4e00' <= character <= '\u9fff', (
        'Input must be a single Chinese character.')
    cc = OpenCC('s2t')
    character = cc.convert(character)
    encoded_character = parse.quote(character.encode('big5'))
    response = requests.get(
        f'https://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/search.php?q={encoded_character}')
    return _parse_response(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('character', type=str, help='The character to be queried.')
    args = parser.parse_args()
    print(get_jyutping_multiple(args.character))
