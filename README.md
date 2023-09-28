# Myanimelist Scraping

![Zero Two](https://github.com/v3xlrm1nOwo1/myanimelist_scraping/assets/87325345/9d06cf62-a0aa-441a-8b50-7622acf1a4b8)

---

Python Scrapy spiders that scrape anime data, reviews and characters information from [Myanimelist.net](https://myanimelist.net/).

This Scrapy project contains one seperate spidersn `myanimelist_spider.py`.

## Explained Myanimelist Scraping:
It starts crawling from [topanime](https://myanimelist.net/topanime.php) and from `anime table` get anime url and follow this url to anime 
page and from `anime page` get all anime data, all reviews url and all characters and voice actors url and follow the `reviews url` for get all reviews data 
and follow the `characters and voice actors url` for get all characters data and all voice actors data and go back to `top anime` page to continue crawling 
when it reaches the last anime in the table, it moves to the next page, after the scraping is finished the data is stored in a `JSON` file.


## ScrapeOps Proxy
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
