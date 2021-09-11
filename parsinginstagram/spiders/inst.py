import re
import scrapy
import json
from urllib.parse import urlencode
from copy import deepcopy
from scrapy.http import HtmlResponse
from parsingInstagram.items import ParsinginstagramItem



class InstSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com']
    request_url = 'https://www.instagram.com/accounts/login/ajax/'
    my_login = 'sanek.ryabov'
    my_passwd = '#PWD_INSTAGRAM_BROWSER:10:1631216145:AbNQADpa4ABehuZAMBzySe4bZXH+R8bRJxcllzc3SMeuqlAwuLOklCHCGG2FyDIYciG5aMo2ZyncPZgusUlIeR3nU4NGfVL2OTj53SrPUBmvnGFPS04vxTVpk6vsT+5TJ+tsIceQQDtxr8+sAC+p50c='
    user_parse = 'ai_machine_learning'
    posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'
    graphql_url = 'https://www.instagram.com/graphql/query/?'

    def parse(self, response: HtmlResponse):
        yield scrapy.FormRequest(self.request_url,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.my_login,
                                           'enc_password': self.my_passwd},
                                 headers={'X-CSRFToken': self.get_csrf_token(response.text)})


    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            yield response.follow(f'/{self.user_parse}',
                                  callback=self.parse_user,
                                  cb_kwargs={'username': self.user_parse})

    def parse_user(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {
            'id': user_id,
            'first': 12
        }
        url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
        yield response.follow(url_posts,
                              callback=self.user_posts_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)}
                              )
    def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):
        if response.status == 200:
            j_data = response.json()
            page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
            if page_info.get('has_next_page'):
                variables['after'] = page_info.get('end_cursor')
                url_posts = f'{self.graphql_url}query_hash={self.posts_hash}&{urlencode(variables)}'
                yield response.follow(url_posts,
                                      callback=self.user_posts_parse,
                                      cb_kwargs={'username': username,
                                                 'user_id': user_id,
                                                 'variables': deepcopy(variables)})

            posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
            for post in posts:
                item = ParsinginstagramItem(user_id=user_id,
                                       username=username,
                                       picture=post.get('node').get('display_url'),
                                       likes=post.get('node').get('edge_media_preview_like').get('count'),
                                       post_data=post.get('node')
                                       )
                yield item


    def get_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"',text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')



