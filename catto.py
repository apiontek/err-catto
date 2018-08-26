import logging
import json
import random
import requests
from errbot import BotPlugin, botcmd

class Catto(BotPlugin):
    """Fetch random cat images URLs"""
    min_err_version = '3.0.0' # Optional, but recommended

    def get_catapi_pic(self, type):
        api_url = 'https://api.thecatapi.com/v1/images/search'
        api_key = '9880edd3-3c4f-4758-aebe-c7182aeb3a70'
        querystring = {"size":"full","mime_types":type,"format":"json","order":"RANDOM","limit":"1"}
        headers = {'Content-Type': "application/json",'x-api-key': api_key}

        try:
            response = requests.request("GET", api_url, headers=headers, params=querystring)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.debug(e)
            return 'Unable to return a cat image'

        return json.loads(response.text)[0]['url']

    def get_randomcat_pic(self):
        api_url = 'http://aws.random.cat/meow'

        try:
            response = requests.request("GET", api_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.debug(e)
            return 'Unable to return a cat image'

        return json.loads(response.text)['file']

    def get_catpic(self):
        choice = random.randint(0, 2)
        if choice < 2:
            return self.get_catapi_pic("jpg,png,gif")
        return self.get_randomcat_pic()

    @botcmd(split_args_with=' ')
    def catto(self, msg, args):
        """Fetch a random cat image, which may be animated (gif) or still (jpg/png)"""
        if len(args) > 0 and args[0]:
            type = args[0]
            if type == 'gif':
                return self.get_catapi_pic("gif")
            elif type == 'still':
                return self.get_catapi_pic("jpg,png")
            else:
                return 'Unrecognized image type. Please use "gif" or "still" or leave blank to get either type.'
        else:
            return self.get_catpic()
