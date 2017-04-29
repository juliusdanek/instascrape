import requests
from lxml import etree
import json
from helpers import extract_email
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
            attributes['id'] = user['id']
            attributes['media_count'] = user['media']['count']
            # attributes['language'] = data_dict['language_code']
            # attributes['country_id'] = data_dict['country_code']
        return attributes

    def retreive_user_media(self, handle, num_media=None):
        url = 'https://www.instagram.com/query/'
        user_attributes = self.bio_scrape(handle)
        user_id = user_attributes['id']
        num_media = num_media if num_media else user_attributes['media_count']
        form_data_raw = 'q=ig_user%28{user_id}%29%20%7B%20media.after%280%2C%20{num_media}%29%20%7B%20%20%20count%2C%20%20%20nodes%20%7B%20%20%20%20%20__typename%2C%20%20%20%20%20caption%2C%20%20%20%20%20code%2C%20%20%20%20%20comments%20%7B%20%20%20%20%20%20%20count%20%20%20%20%20%7D%2C%20%20%20%20%20comments_disabled%2C%20%20%20%20%20date%2C%20%20%20%20%20dimensions%20%7B%20%20%20%20%20%20%20height%2C%20%20%20%20%20%20%20width%20%20%20%20%20%7D%2C%20%20%20%20%20display_src%2C%20%20%20%20%20id%2C%20%20%20%20%20is_video%2C%20%20%20%20%20likes%20%7B%20%20%20%20%20%20%20count%20%2C%20id%20%20%20%20%7D%2C%20%20%20%20%20owner%20%7B%20%20%20%20%20%20%20id%20%20%20%20%20%7D%2C%20%20%20%20%20thumbnail_src%2C%20%20%20%20%20video_views%20%20%20%7D%2C%20%20%20page_info%20%7D%20%20%7D'
        form_data = form_data_raw.format(user_id=user_id, num_media=num_media)
        headers = {
            'x-csrftoken': self.session.cookies['csrftoken'],
            'referer': 'https://www.instagram.com/{}/'.format(handle),
            'x-instagram-ajax': '1',
            'x-requested-with': 'XMLHttpRequest',
            'content-type': 'application/x-www-form-urlencoded',

        }
        response = self.session.post(url, headers=headers, data=form_data)
        response.raise_for_status()
        return response.json()


if __name__ == '__main__':
    client = InstaClient()
    print client.bio_scrape('kaptenandson')
    user_media = client.retreive_user_media('kaptenandson')
    import ipdb; ipdb.set_trace()
