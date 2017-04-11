instascrape
-----------

A small library that allows you to scrape Instagram – limited to biographies, follower numbers, emails and external URLs for now.

To use, simply do:

| In [1]: import instascrape

| In [2]: instascrape.bio_scrape('9gag')
| Out[2]:
|  {'bio': u'The best content platform for millennials \u2022 Share your content with our 150M | global audience \u2022 \U0001f4e7 creation@9gag.com \u2022',
|  'email': u'creation@9gag.com',
|  'external_url': 'http://9gag.com/apps',
|  'followers': 38911657,
|  'ig_handle': '9gag',
|  'ig_url': 'https://www.instagram.com/9gag/'}

Sample

Please make sure to input the Instagram handle of the profile you are trying to scrape, not the entire url.
