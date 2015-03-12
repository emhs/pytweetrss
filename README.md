PyTweetRSS
==========

A simple python-based command-line tool to poll a feed regularly and tweet the results. Tweets are posted with randomized waits to ensure an organic feel to the timelines. Only compatible with Python 2.x

## Installation

    $ git clone https://www.github.com/emhs/pytweetrss
    $ cd pytweetrss
	# python setup.py install

## Configuration

PyTweetRSS is configured using an INI-style config file located at `~/.pytweetrss`. I've provided an example config file that you can copy to that location. The following values need to be specified (everything else can be left at the defaults):

* url — Set this to the URL of the feed you wish to poll
* suffix — Set this to the suffix you wish to attach to the end of the URL, without any leading "?"
* Bit.ly username — Provide your Bit.ly username here
* Bit.ly api_key — Provide the legacy API key from Bit.ly's settings page

Leave the Twitter settings blank. They'll be filled in automatically on the first run. 

## Usage

`$ pytweetrss`

On the first run, the command will attempt to open your web browser to authenticate in Twitter. If this fails, simply copy and paste the URL it provides into a browser, authenticate, and then give the program the pincode that Twitter provides. The process will start right up, and begin processing the RSS feed from oldest to newest. Tweets will be posted between one and three minutes. Once it's caught up, it will poll between 5 and 10 minutes, and then post additional tweets as more are located.

Good luck, and enjoy.
