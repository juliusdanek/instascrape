import requests
from lxml import etree
import json
from .helpers import extract_email
import random


class InstaClient(object):
    def __init__(self, proxies=None):
        user_agent = random.choice([
            "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.600.0 Safari/534.14",
            "Mozilla/5.0 (X11; U; Windows NT 6; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.11 Safari/534.16",
            "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.792.0 Safari/535.1",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.872.0 Safari/535.2",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
            "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19"
        ])
        self.session = requests.Session()
        self.session.headers = {"User-Agent": user_agent}
        if proxies:
            self.session.proxies.update(proxies)

    def bio_scrape(self, handle):
        """
        Take the instagram handle as input, like '9gag' Will return a dictionary containing the following attributes:
        - followers: number of followers
        - biography: profile biography
        - email: email if listed in profile biograhy
        - external_url: external URL if exists
        """
        url = 'https://www.instagram.com/{}/'.format(handle)
        attributes = {}
        response = self.session.get(url)
        response.raise_for_status()
        if response.ok:
            root = etree.HTML(response.content)
            data_raw = root.xpath("//script[contains(text(), 'entry_data')]")[0].text
            data_raw = data_raw[data_raw.find('{'): data_raw.rfind('}') + 1]
            data_dict = json.loads(data_raw)
            user = data_dict['entry_data']['ProfilePage'][0]['user']
            bio = user['biography']
            attributes['email'] = extract_email(bio)
            attributes['followed_by'] = user['followed_by']['count']
            attributes['is_verified'] = user['is_verified']
            attributes['follows'] = user['follows']['count']
            attributes['profile_pic_url'] = user['profile_pic_url_hd']
            attributes['external_url'] = user['external_url']
            attributes['bio'] = bio
            attributes['ig_handle'] = handle
            attributes['ig_url'] = url
            attributes['ig_id'] = user['id']
            attributes['media_count'] = user['media']['count']
            # attributes['language'] = data_dict['language_code']
            # attributes['country_id'] = data_dict['country_code']
        return (attributes, data_dict)

    def retreive_user_media(self, handle, num_media=None, cursor=None):
        url = 'https://www.instagram.com/graphql/query/'
        user_attributes = self.bio_scrape(handle)
        user_id = user_attributes['id']
        num_media = num_media if num_media else user_attributes['media_count']
        payload = {
            "query_id": "17880160963012870",
            "id": user_id,
            "first": num_media,
            "after": cursor
        }
        response = self.session.get(url, params=payload)
        response.raise_for_status()
        return response.json()


if __name__ == '__main__':
    client = InstaClient()
    print(client.bio_scrape('instagram'))
    #num_media is needed for accounts with 2000+ posts
    user_media = client.retreive_user_media(handle='instagram', num_media=10)
    print(user_media.keys())
    import ipdb; ipdb.set_trace()
