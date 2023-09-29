import scrapy
from myanimelist_scraper.items import MyanimelistScraperItem
from scrapy.utils.defer import maybe_deferred_to_future



class MyanimelistSpiderSpider(scrapy.Spider):
    name = 'myanimelist_spider'
    allowed_domains = ['myanimelist.net', 'proxy.scrapeops.io']
    start_urls = ['https://myanimelist.net/topanime.php']

    
    custom_settings = {
        'FEEDS': {
            'anime_data.json': { 'format': 'json', 'overwrite': True},
            }
        }


    def parse(self, response):
        table = response.css('table.top-ranking-table')[0]
        all_anime = table.css('tr.ranking-list')
        
        for anime in all_anime:
            anime_url = str(anime.css('td div.detail div h3 a  ::attr(href)').get()).strip()
            if anime_url is not None:
                yield response.follow(url=anime_url, callback=self.parse_anime_page)
        
        
        next_page = response.css('div.pagination a.next ::attr(href)').get()
        
        if next_page is not None:
            next_page_url = f'https://myanimelist.net/topanime.php{next_page}'
            yield response.follow(url=next_page_url, callback=self.parse)

    # get all anime information
    def parse_anime_page(self, response):
        row_table = response.css('div#contentWrapper div#content table tr')

        url = response.url

        resp_meta = {
            'rank': str(row_table.css('td div.pb16 div.di-t div div div.di-ib span.ranked strong ::text').get()).strip(),
            'popularity': str(row_table.css('td div.pb16 div.di-t div div div.di-ib span.popularity strong ::text').get()).strip(),
            'en_name': str(response.css('div div div.h1 div.h1-title div h1.title-name strong ::text').get()).strip(),
            'jp_name': [key.get() for key in [key.css(' ::text') for key in row_table.css('td.borderClass div.leftside div.spaceit_pad') if key.css('span.dark_text ::text').get() == 'Japanese:'][0] if str(key.get()).strip() != '' and str(key.get()).strip() != ',' and str(key.get()).strip() != 'Japanese:'][0].strip(),
            'image': row_table.css('td.borderClass div.leftside div a img[itemprop="image"]::attr(data-src)').get().strip(),
            'description': [des.get() for des in  row_table.css('td div table tr td p[itemprop="description"]::text')],
            'genre': [genre.css('::text').get() for genre in row_table.css('td.borderClass div.leftside div span[itemprop="genre"]')],
            'score': row_table.css('td div.pb16 div.di-t div div div div.score-label::text').get(),
            'members': [key.css(' ::text')[-1].get() for key in row_table.css('td.borderClass div.leftside div.spaceit_pad') if key.css('span.dark_text ::text').get() == 'Members:'],
            'favorites': [key.css(' ::text')[-1].get() for key in row_table.css('td.borderClass div.leftside div.spaceit_pad') if key.css('span.dark_text ::text').get() == 'Favorites:'],
            'rating': [key.css(' ::text')[-1].get() for key in row_table.css('td.borderClass div.leftside div.spaceit_pad') if key.css('span.dark_text ::text').get() == 'Rating:'],
            'duration': [key.css(' ::text')[-1].get() for key in row_table.css('td.borderClass div.leftside div.spaceit_pad') if key.css('span.dark_text ::text').get() == 'Duration:'],
            'aired': [key.css(' ::text')[-1].get() for key in row_table.css('td.borderClass div.leftside div.spaceit_pad') if key.css('span.dark_text ::text').get() == 'Aired:'],
            'episodes': [key.css(' ::text')[-1].get() for key in row_table.css('td.borderClass div.leftside div.spaceit_pad') if key.css('span.dark_text ::text').get() == 'Episodes:'],
            'scurce': [key.css(' ::text')[-1].get() for key in row_table.css('td.borderClass div.leftside div.spaceit_pad') if key.css('span.dark_text ::text').get() == 'Source:'],
            'scored_by': [key.css(' ::text')[6].get() for key in row_table.css('td.borderClass div.leftside div.spaceit_pad') if key.css('span.dark_text ::text').get() == 'Score:'],
            'studios': [key.get() for key in [key.css(' ::text') for key in row_table.css('td.borderClass div.leftside div.spaceit_pad') if key.css('span.dark_text ::text').get() == 'Studios:'][0] if str(key.get()).strip() != '' and str(key.get()).strip() != ',' and str(key.get()).strip() != 'Studios:'],
            'url': str(url).strip()
            }

        # go to reviews
        reviews_page_url = f'{url}/reviews&spoiler=on'
        yield response.follow(url=reviews_page_url, callback=self.parse_get_reviews, meta=resp_meta)
    

    # get all anime reviews
    def parse_get_reviews(self, response):

        reviews_data = response.css('div[id="contentWrapper"] div[id="content"] table tr td[valign="top"] div[class="rightside js-scrollfix-bottom-rel"] div[class="review-element js-review-element"] div[class="thumbbody mt8"]')

        reviews = []
        for review_data in reviews_data:

            resp_review_data = {
                'username': str(review_data.css('div.body div.username a::text').get()).strip(),
                'user_img': str(review_data.css('div.thumb a img::attr(src)').get()).strip(),
                'user_link': str(review_data.css('div.body div.username a::attr(href)').get()).strip(),
                'review_text': ''.join(review_data.css('div.body div.text').getall()).strip(),
                'tag': str(review_data.css('div.body div.tags div::text').get()).strip(),
                'reviewers_rating': str(review_data.css('div.body div[class="rating mt20 mb20 js-hidden"] span.num ::text').get()).strip(),
                'reactions': [(reaction.css('::text').get(), reaction.css('span.num ::text').get(), reaction.css('img::attr(src)').get()) for reaction in review_data.css('div.body div.reaction-box div')],
            }
            
            reviews.append(resp_review_data)
            
        resp_meta = {
            **response.request.meta,
            'reviews': reviews
        }

        # next reviews page
        next_reviews_page = response.css('div[id="contentWrapper"] div[id="content"] table tr td[valign="top"] div.mt4 div[class="ml4 mb8"] a ::attr(href)').get()
        if next_reviews_page is not None:
            yield response.follow(url=next_reviews_page, callback=self.parse_get_reviews)
        
        else:
            # go to characters and voice actors
            try:
                characters_and_voice_actors_page_url = f'{response.request.meta["url"]}/characters'
                yield response.follow(url=characters_and_voice_actors_page_url, callback=self.parse_get_characters_and_voice_actors, meta=resp_meta)
            except:
                print(f'*************!!!!None Data**************\n\n{characters_and_voice_actors_page_url}\n\n{response.request.meta}\n\n')


    # get all anime characters and voice actors
    async def parse_get_characters_and_voice_actors(self, response):
        resp_meta = {
            **response.request.meta,
            'characters_information': [],
            }
        
        characters_url = response.css('table[class="js-anime-character-table"] tr td[valign="top"] div.spaceit_pad a::attr(href)').getall()
        characters_url = [char_url for char_url in characters_url if char_url.find('character') != -1]

        for idx, char_url in enumerate(characters_url):
            
            if char_url is not None:
                request = scrapy.Request(char_url.strip())
                response = await maybe_deferred_to_future(self.crawler.engine.download(request))
                char_information = response.css('table tr td[valign="top"]::text').getall()
                char_information = [char_info.strip() for char_info in char_information if char_info.strip() != '']

                all_data = response.css('table tr td[valign="top"]')
                all_data = all_data.css('::text').getall()
                all_data = [data.strip() for data in all_data if data.strip() != '']

                all_char_information = all_data[all_data.index(char_information[1]): all_data.index(char_information[-1]) + 1]
                all_char_information.insert(0, char_information[0])

                char_information_dict = {'char_description': ''}

                for idx, char_info in enumerate(all_char_information):
                    char_info = char_info.strip()
                    if char_info != '':
                        char_info = char_info.split(': ')
                        if len(char_info) == 2:
                            char_information_dict['_'.join(char_info[0].strip().lower().split()).strip()] = char_info[1].strip()
                        else:
                            char_information_dict['char_description'] += ' ' + char_info[0].strip()

                # voice actors data
                voice_actors_data = response.css('table table')[2: ]
                voice_actors_data_list = []
                for idx, voice_actor in enumerate(voice_actors_data):
                    voice_actor_data = {
                        'name': str(voice_actor.css('tr td.borderClass a::text').get()).strip(),
                        'image': str(voice_actor.css('tr td div.picSurround a img::attr(data-src)').get()).strip(),
                        'country': str(voice_actor.css('tr td.borderClass div small::text').get()).strip(),
                        }
                    voice_actors_data_list.append(voice_actor_data)

                # all character information
                char = {
                    'image': str(response.css('table tr td.borderClass div a img::attr(data-src)').get()).strip(),
                    'en_name': str(response.css('table tr td[valign="top"] h2.normal_header::text').get()).strip(),
                    'jp_name': str(response.css('table tr td[valign="top"] h2.normal_header span small::text').get()).strip(),
                    **char_information_dict,
                    'voice_actors': voice_actors_data_list,
                    }
                
                resp_meta['characters_information'].append({str(response.css('table tr td[valign="top"] h2.normal_header::text').get()).strip(): char})

        yield response.follow(url='None', callback=self.parse_combine_data, meta=resp_meta)


    # combine all data
    def parse_combine_data(self, response):

        # anime data
        anime_item = MyanimelistScraperItem()
        anime_item['rank'] = response.request.meta['rank']
        anime_item['popularity'] = response.request.meta['popularity']
        anime_item['en_name'] = response.request.meta['name_en']
        anime_item['jp_name'] = response.request.meta['name_jp']
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

 