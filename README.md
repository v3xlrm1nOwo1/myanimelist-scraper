# Myanimelist Scraper

> Zero Two is Love <3

![Zero Two](https://github.com/v3xlrm1nOwo1/myanimelist_scraping/assets/87325345/9d06cf62-a0aa-441a-8b50-7622acf1a4b8)

---

Python Scrapy spiders that scrape anime data, reviews and characters information from [Myanimelist.net](https://myanimelist.net/).

This Scrapy project contains one seperate spidersn `myanimelist_spider.py`.

## Explained Myanimelist Scraping:
It starts crawling from [topanime](https://myanimelist.net/topanime.php) and from `anime table` get anime url and follow this url to anime 
page and from `anime page` get all anime data, all reviews url and all characters and voice actors url and follow the `reviews url` for get all reviews data 
and follow the `characters and voice actors url` for get all characters data and all voice actors data and go back to `top anime` page to continue crawling 
when it reaches the last anime in the table, it moves to the next page, after the scraping is finished the data is stored in a `JSON` file.


## Avoid Blocking:

### 1 - Customize Middleware:

#### Fake User Agent:

> `middleware.py`

```py
from urllib.parse import urlencode
from random import randint
import requests

class ScrapeOpsFakeUserAgentMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT', 'http://headers.scrapeops.io/v1/user-agents?') 
        self.scrapeops_fake_user_agents_active = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENABLED', False)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self._get_user_agents_list()
        self._scrapeops_fake_user_agents_enabled()


    def _get_user_agents_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.user_agents_list = json_response.get('result', [])


    def _get_random_user_agent(self):
        random_index = randint(0, len(self.user_agents_list) - 1)
        return self.user_agents_list[random_index]

    def _scrapeops_fake_user_agents_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_user_agents_active == False:
            self.scrapeops_fake_user_agents_active = False
        else:
            self.scrapeops_fake_user_agents_active = True

    def process_request(self, request, spider):        
        random_user_agent = self._get_random_user_agent()
        request.headers['User-Agent'] = random_user_agent

        print("************ NEW HEADER ATTACHED *******")
        print(request.headers['User-Agent'])
```

> `settings.py`

```py
SCRAPEOPS_API_KEY =  config.API_KEY  # signup at https://scrapeops.io
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = 'https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = False
SCRAPEOPS_NUM_RESULTS = 100

DOWNLOADER_MIDDLEWARES = {
    'myanimelist_scraper.middlewares.myanimelist_scraperDownloaderMiddleware': 543,
    'myanimelist_scraper.middlewares.ScrapeOpsFakeUserAgentMiddleware': 450,
}
```
#### ScrapeOps Fake Browser Header Agent:
> `middleware.py`

```py
class ScrapeOpsFakeBrowserHeaderAgentMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT', 'http://headers.scrapeops.io/v1/browser-headers') 
        self.scrapeops_fake_browser_headers_active = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED', True)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self._get_headers_list()
        self._scrapeops_fake_browser_headers_enabled()

    def _get_headers_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.headers_list = json_response.get('result', [])

    def _get_random_browser_header(self):
        random_index = randint(0, len(self.headers_list) - 1)
        return self.headers_list[random_index]

    def _scrapeops_fake_browser_headers_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_browser_headers_active == False:
            self.scrapeops_fake_browser_headers_active = False
        else:
            self.scrapeops_fake_browser_headers_active = True
    
    def process_request(self, request, spider):        
        random_browser_header = self._get_random_browser_header()

        request.headers['accept-language'] = random_browser_header['accept-language']
        request.headers['sec-fetch-user'] = random_browser_header['sec-fetch-user'] 
        request.headers['sec-fetch-mod'] = random_browser_header['sec-fetch-mod'] 
        request.headers['sec-fetch-site'] = random_browser_header['sec-fetch-site'] 
        request.headers['sec-ch-ua-platform'] = random_browser_header['sec-ch-ua-platform'] 
        request.headers['sec-ch-ua-mobile'] = random_browser_header['sec-ch-ua-mobile'] 
        request.headers['sec-ch-ua'] = random_browser_header['sec-ch-ua'] 
        request.headers['accept'] = random_browser_header['accept'] 
        request.headers['user-agent'] = random_browser_header['user-agent'] 
        request.headers['upgrade-insecure-requests'] = random_browser_header.get('upgrade-insecure-requests')
    

        print("************ NEW HEADER ATTACHED *******")
        print(request.headers)
```

> `settings.py`

```py
DOWNLOADER_MIDDLEWARES = {
    'myanimelist_scraper.middlewares.myanimelist_scraperDownloaderMiddleware': 543,
    'myanimelist_scraper.middlewares.ScrapeOpsFakeUserAgentMiddleware': 450,
    'myanimelist_scraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware': 400,
}
```


#### Proxy:
> `Terminal`

```zsh
pip install scrapy-rotating-proxies
```

> `settings.py`

```py
ROTATING_PROXY_LIST_PATH = # Here put PROXY list or text file path

DOWNLOADER_MIDDLEWARES = {
    'myanimelist_scraper.middlewares.myanimelist_scraperDownloaderMiddleware': 543,
    'myanimelist_scraper.middlewares.ScrapeOpsFakeUserAgentMiddleware': 450,
    'myanimelist_scraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware': 400,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}
```

### 2 - Using ScrapeOps:

#### ScrapeOps Proxy:
This Myanimelist spider uses [ScrapeOps Proxy](https://scrapeops.io/proxy-aggregator/) as the proxy solution. ScrapeOps has a free plan that allows you to make up to 1,000 requests per month which makes it ideal for the development phase, but can be easily scaled up to millions of pages per month if needs be.

You can [sign up for a free API key here](https://scrapeops.io/app/register/main).

To use the ScrapeOps Proxy you need to first install the proxy middleware:

```python
pip install scrapeops-scrapy-proxy-sdk
```

Then activate the ScrapeOps Proxy by adding your API key to the `SCRAPEOPS_API_KEY` in the ``settings.py`` file.

```python
SCRAPEOPS_API_KEY = 'YOUR_API_KEY'

SCRAPEOPS_PROXY_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}
```


## Running The Scrapers:
- frist install scrapy and install the proxy middleware
    ```zsh
    pip install scrapy scrapeops-scrapy-proxy-sdk
    ```

- create `config.py` and save API KEY
  ```zsh
  echo API_KEY = 'api key' > config.py
  ```

- finaly Then to run the spider, enter one of the following command:
  ```zsh
  scrapy crawl myanimelist_spider
  ```

## Explantion the Extracted Data:

```py
def parse_combine_data(self, response):
      # anime data
      anime_item = MyanimelistScraperItem()
      anime_item['rank'] = response.request.meta['rank']
      anime_item['popularity'] = response.request.meta['popularity']
      anime_item['name'] = response.request.meta['name']
      anime_item['image'] = response.request.meta['image']
      anime_item['description'] = response.request.meta['description']
      anime_item['genre'] = response.request.meta['genre']
      anime_item['score'] = response.request.meta['score']
      anime_item['members'] = response.request.meta['members']
      anime_item['favorites'] = response.request.meta['favorites']
      anime_item['rating'] = response.request.meta['rating']
      anime_item['duration'] = response.request.meta['duration']
      anime_item['aired'] = response.request.meta['aired']
      anime_item['episodes'] = response.request.meta['episodes']
      anime_item['scurce'] = response.request.meta['scurce']
      anime_item['scored_by'] = response.request.meta['scored_by']
      anime_item['studios'] = response.request.meta['studios']
      anime_item['url'] = response.request.meta['url']

      # review data
      anime_item['reviews'] = response.request.meta['reviews']

      # character data
      anime_item['characters_information'] = response.request.meta['characters_information']

      yield anime_item
```

### Explained Columns:
> all columns name:

| Fiels  |      Description      |       Data Type       |
|--------|-----------------------|-----------------------|
| `name` |  anime name. | String |
| `rank` |  anime rank. | Integer |
| `popularity` |  anime popularity. | Integer | 
| `name` |  anime name. | String |
|`image`  |  anime cover image.    |    String   |
|`description`  |  anime description.  |    String    |
|`genre`  |  all anime genre.   |    List     |
|`score`  |  anime score.   |    Integer    |
|`url`  |  page amime url.   |    String    |
|`members`  |  anime members.   |    Integer    |
|`favorites`  |  anime favorites.   |    Integer    |
|`rating`  |  anime rating.   |    Integer    |
|`duration`  |  anime episode time.   |    String    |
|`aired`  |  anime aired.   |    Sgtring    |
|`episodes`  |  number of anime episodes   |    Integer    |
|`scurce`  |  origin anime scurce.   |    String   |
|`scored_by`  |  number of user scored by.    |    Integer    |
|`studios`  |  all studios animes.  |    List    |
|`reviews`  |  it's a list of dictionary contains all reviews data.   |    List    |
|`characters_information`  |  it's a list of dictionary contains all characters information and voice actors.    |    List   |


After the scraping is finished the data is stored in a `JSON` file.

`settings.py`
```py
FEEDS = {
    'anime_data.json': {'format': 'json', 'overwrite': True}
}
```

`myanimelist_spider.py`
```py
custom_settings = {
  'FEEDS': {
    'anime_data.json': { 'format': 'json', 'overwrite': True},
    }
}
```

----

# Don't Forget to Put a Star 🌟

## Star History

<a href="https://star-history.com/#v3xlrm1nOwo1/myanimelist_scraping&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=v3xlrm1nOwo1/myanimelist_scraping&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=v3xlrm1nOwo1/myanimelist_scraping&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=v3xlrm1nOwo1/myanimelist_scraping&type=Date" />
  </picture>
</a>


