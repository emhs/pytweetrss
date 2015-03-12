# -*- coding: utf-8 -*-

"""PyTweetRSS --- A RSS-to-Twitter daemon"""

import twitter
import feedparser
import click
import os
import ConfigParser
import bitly_api
import webbrowser
from requests_oauthlib import OAuth1Session
import time
import random

config = ConfigParser.RawConfigParser()

config.read(os.path.join(os.environ['HOME'], '.pytweetrss'))

def shorten(link):
    user = config.get('Bit.ly', 'username')
    key = config.get('Bit.ly', 'api_key')
    bitly = bitly_api.Connection(user, key)
    return(bitly.shorten(link))

def poll_feed():
    url = config.get('General', 'url')
    parser = feedparser.parse(url)
    return(parser.entries)

def make_tweet(entry):
    title = entry.title
    link = entry.link
    overflow = config.get('General', 'overflow')
    suffix = config.get('General', 'suffix')

    if overflow == 'ellipsis':
        while len(title) > 115:
            words = title.split(u' ')
            title = u' '.join(words[:-1]) + u'…'

    if suffix and '?' in link:
        link += '&' + suffix
    else:
        link += '?' + suffix

    tweet = title + u" — " + shorten(link)['url']
    return(tweet)

def parse_feed(last_seen):
    entries = poll_feed()
    tweets = [make_tweet(entry) for entry in entries]
    try:
        tweets = tweets[:tweets.index(last_seen)]
    except ValueError:
        pass
    return(tweets)

@click.command()
def main():
    """Poll a feed for updates and tweet them"""

    consumer_key = 'u9bRLlFuXaG92ZsMiZZC4UiXt'
    consumer_secret = '7h5h2SYX9HZY81PUzfhpKdQcCmrDANziEEZfHESyJCvr0LXqmz'
    if not config.get('Twitter', 'token'):
        request_token_url = 'https://api.twitter.com/oauth/request_token'
        access_token_url = 'https://api.twitter.com/oauth/access_token'
        authorization_url = 'https://api.twitter.com/oauth/authorize'
        signin_url = 'https://api.twitter.com/oauth/authenticate'
        oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret)

        click.echo('Requesting temp token from Twitter')
        try:
            resp = oauth_client.fetch_request_token(request_token_url)
        except ValueError, e:
            click.echo('Invalid response from Twitter requesting temp token: {}'.format(e), err=True)
            return()
        a_url = oauth_client.authorization_url(authorization_url)

        click.echo('')
        click.echo('Trying to start a browser for Twitter authentication. If')
        click.echo('the browser does not start automatically, please copy the')
        click.echo('URL below into a browser, sign in using Twitter, and')
        click.echo('retrieve the pincode provided.')
        click.echo('')
        click.echo(url)
        click.echo('')

        webbrowser.open(a_url)
        pincode = raw_input('Pincode? ')

        click.echo('')
        click.echo('Generating and signing OAuth request for an access token')
        click.echo('')

        oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret,
                                     resource_owner_key=resp.get('oauth_token'),
                                     resource_owner_secret=resp.get('oauth_token_secret'),
                                     verifier=pincode)
        try:
            resp = oauth_client.fetch_access_token(access_token_url)
        except ValueError, e:
            click.echo('Invalid response from Twitter requesting access token: {}'.format(e), err=True)
            return()
        twitter_token = resp.get('oauth_token')
        twitter_secret = resp.get('oauth_token_secret')
        config.set('Twitter', 'token', twitter_token)
        config.set('Twitter', 'secret', twitter_secret)
        with open(
                os.path.join(
                    os.environ['HOME'], '.pytweetrss'), 'w') as conf_file:
            config.write(conf_file)

    last_seen = ''
    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=config.get('Twitter', 'token'),
                      access_token_secret=config.get('Twitter', 'secret'))
    click.echo('Opened Twitter API connection')
    while True:
        click.echo('Parsing feed...')
        tweets = parse_feed(last_seen)
        click.echo('Done.')
        if tweets:
            click.echo('Got entries to tweet:')
            last_seen = tweets[0]
            tweets = tweets[::-1]
            for tweet in tweets:
                api.PostUpdate(tweet)
                click.echo(tweet)
                time.sleep(random.randint(60,180))
            config.set('General', 'last_seen', last_seen)
            with open(
                    os.path.join(
                        os.environ['HOME'], '.pytweetrss'), 'w') as conf_file:
                config.write(conf_file)
        time.sleep(random.randint(300,600))

if __name__ == "__main__":
    main()
