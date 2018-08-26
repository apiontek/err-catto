import logging
import json
import random
import requests
from errbot import BotPlugin, botcmd
from itertools import chain

CONFIG_TEMPLATE = {'CATAPI_KEY': '9880edd3-3c4f-4758-aebe-c7182aeb3a70'}

class Catto(BotPlugin):
    """Fetch random cat images URLs"""
    min_err_version = '3.0.0' # Optional, but recommended

    def get_configuration_template(self):
        return CONFIG_TEMPLATE

    def configure(self, configuration):
        if configuration is not None and configuration != {}:
            config = dict(chain(CONFIG_TEMPLATE.items(),
                                configuration.items()))
        else:
            config = CONFIG_TEMPLATE
        super(Catto, self).configure(config)

    def get_catapi_pic(self, type):
        api_url = 'https://api.thecatapi.com/v1/images/search'
        querystring = {"size":"full","mime_types":type,"format":"json","order":"RANDOM","limit":"1"}
        headers = {'Content-Type': "application/json",'x-api-key': self.config['CATAPI_KEY']}

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
        """Fetch a random cat image, optionally specifying 'gif' (animated), 'still' (jpg or png), or 'jpg' or 'png'"""
        if len(args) > 0 and args[0]:
            type = args[0]
            if type == 'gif':
                return self.get_catapi_pic("gif")
            elif type == 'still':
                return self.get_catapi_pic("jpg,png")
            elif type == 'jpg':
                return self.get_catapi_pic(type)
            elif type == 'png':
                return self.get_catapi_pic(type)
            else:
                return 'Unrecognized image type. Please use "gif", "still", "jpg", "png", or leave blank to get any type.'
        else:
            return self.get_catpic()
