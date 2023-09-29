# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


def serialize_rank_popularity(value):
    return int(str(value).strip()[1: ])


class MyanimelistScraperItem(scrapy.Item):
    # define the fields for your item here like:
    
    # anime
    en_name = scrapy.Field()
    jp_name = scrapy.Field()
    rank = scrapy.Field(serializer=serialize_rank_popularity)
    popularity = scrapy.Field(serializer=serialize_rank_popularity)
    image = scrapy.Field()
    description = scrapy.Field()
    genre = scrapy.Field()
    score = scrapy.Field()
    url = scrapy.Field()
    members = scrapy.Field()
    favorites = scrapy.Field()
    rating = scrapy.Field()
    duration = scrapy.Field()
    aired = scrapy.Field()
    episodes = scrapy.Field()
    scurce = scrapy.Field()
    scored_by = scrapy.Field()
    studios = scrapy.Field()

    # reviews
    reviews = scrapy.Field()
    
    # characters
    characters_information = scrapy.Field()