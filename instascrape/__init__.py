import requests
from lxml import etree
import ast
from helpers import extract_email


def bio_scrape(handle, proxies=None):
    """
    Take the instagram handle as input, like '9gag' Will return a dictionary containing the following attributes:
    - followers: number of followers
    - biography: profile biography
    - email: email if listed in profile biograhy
    - external_url: external URL if exists
    """
    url = 'https://www.instagram.com/{}/'.format(handle)
    attributes = {}
    response = requests.get(url, proxies=proxies)
    response.raise_for_status()
    if response.ok:
        root = etree.HTML(response.content)
        data_raw = root.xpath("//script[contains(text(), 'entry_data')]")[0].text
        data_raw = data_raw[data_raw.find('{'): data_raw.rfind('}') + 1]
        data_raw = data_raw.replace('false', 'False')
        data_raw = data_raw.replace('true', 'True')
        data_raw = data_raw.replace('null', 'None')
        data_dict = ast.literal_eval(data_raw)
        user = data_dict['entry_data']['ProfilePage'][0]['user']
        # decode javascript escape, see http://stackoverflow.com/questions/25457598/how-do-i-decode-escaped-unicode-javascript-code-in-python
        bio = user['biography'].decode('unicode-escape')
        attributes['email'] = extract_email(bio)
        attributes['followers'] = user['followed_by']['count']
        attributes['external_url'] = user['external_url']
        attributes['bio'] = bio
        attributes['ig_handle'] = handle
        attributes['ig_url'] = url
        # attributes['language'] = data_dict['language_code']
        # attributes['country_id'] = data_dict['country_code']
    return attributes
