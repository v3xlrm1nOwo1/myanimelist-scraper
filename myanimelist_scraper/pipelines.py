# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class MyanimelistScraperPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item=item)
        field_names = adapter.field_names()
        
        for field_name in field_names:
            
            if field_name == 'description':
                value = adapter.get(field_name)
                description = ''
                for row in value:
                    row = row.strip()
                    if row.find('[Written by') == -1:
                        description += row + ' '
                    else:
                        description = description
                adapter[field_name] = description.strip()
                

            elif field_name == 'score':
                value = adapter.get(field_name)
                
                adapter[field_name] = float(value)

            
            elif field_name == 'members' or field_name == 'favorites':
                value = adapter.get(field_name)
                value = value[0].strip().split(',')
                int_value = ''
                for val in value:
                    int_value += val
                adapter[field_name] = int(int_value)


            elif field_name == 'rating' or field_name == 'duration' or field_name == 'aired' or field_name == 'scurce':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()

            
            elif field_name == 'scored_by' or field_name == 'episodes':
                value = adapter.get(field_name)
                adapter[field_name] = int(str(value[0]).strip())


            elif field_name == 'studios':
                value = adapter.get(field_name)
                adapter[field_name] = value

            
            elif field_name == 'reviews':
                review_list = adapter.get(field_name)

                new_review_list = list()

                for review_dict in review_list:
                    new_review_dict = dict()

                    for key, value in review_dict.items():

                        if key == 'username' or key == 'user_img' or key == 'user_link' or key == 'tag':
                            new_review_dict[key] = value.strip()

                        elif key == 'reviewers_rating':
                            new_review_dict[key] = int(value.strip())

                        elif key == 'review_text':
                            new_review_dict[key] = self._clean_text(value)

                        else:
                            new_review_dict[key] = value
                        
                    new_review_list.append(new_review_dict)
                adapter[field_name] = new_review_list


            elif field_name == 'characters_information':
                characters_info_list = adapter.get(field_name)

                new_characters_info_list = list()

                for character_info_dict in characters_info_list:

                    new_character_info_dict = dict()

                    for key, value in character_info_dict.items():
                        
                        if key == 'image' or key == 'en_name' or key == 'jp_name':
                            new_character_info_dict[key] = value.strip()

                        elif key == 'char_description':
                            new_character_info_dict[key] = self._clean_text(value)

                        else:
                            new_character_info_dict[key] = value

                    new_characters_info_list.append(new_character_info_dict)
                adapter[field_name] = new_characters_info_list

        return item
    
    
    def _clean_text(self, text):
        clean_text = re.compile(r'<.*?>')
        return clean_text.sub('', text).strip()
    
