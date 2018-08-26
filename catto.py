#import re
import json
import random
import logging
import requests
from errbot import BotPlugin, botcmd, re_botcmd

class Catto(BotPlugin):
    """Plugin for random cat images!"""
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
        flip = random.randint(0, 1)
        if flip == 0:
            return self.get_catapi_pic("jpg,png,gif")
        return self.get_randomcat_pic()

    @botcmd()
    def catto(self, msg, args):
        """Retrieve a random cat image, which may be animated (gif) or still (jpg/png)"""
        if "gif" in args:
            return self.catto_gif(msg, args)
        elif "still" in args:
            return self.catto_still(msg, args)
        return self.get_catpic()

    @botcmd()
    def catto_gif(self, msg, args):
        """Retrieve a random cat animated gif"""
        return self.get_catapi_pic("gif")
    
    @botcmd()
    def catto_still(self, msg, args):
        """Retrieve a random cat still picture (not animated)"""
        return self.get_catapi_pic("jpg,png")


    # @botcmd
    # def catto_gif(self, msg, args):
    #     """Retrieve a random cat image"""
    #     return self.get_catpic("gif")

    # """Example 'Hello, world!' plugin, modified by APiontek"""

    # @botcmd
    # def hello(self, msg, args):
    #     """Say hello to the world"""
    #     return "Fart on this, fucker!!"

    # @re_botcmd(pattern=r"^(([Cc]an|[Mm]ay) I have a )?cookie please\?$")
    # def hand_out_cookies(self, msg, match):
    #     """
    #     Gives cookies to people who ask me nicely.

    #     This command works especially nice if you have the following in
    #     your `config.py`:

    #     BOT_ALT_PREFIXES = ('Err',)
    #     BOT_ALT_PREFIX_SEPARATORS = (':', ',', ';')

    #     People are then able to say one of the following:

    #     Err, can I have a cookie please?
    #     Err: May I have a cookie please?
    #     Err; cookie please?
    #     """
    #     yield "Here's a cookie for you, {}".format(msg.frm)
    #     yield "/me hands out a cookie."

    # @re_botcmd(pattern=r"(^| )cookies?( |$)", prefixed=False, flags=re.IGNORECASE)
    # def listen_for_talk_of_cookies(self, msg, match):
    #     """Talk of cookies gives Errbot a craving..."""
    #     return "Somebody mentioned cookies? Om nom nom!"
