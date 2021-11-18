import markovify
import MeCab
import json
from markovify import text
import tweepy
from read_data import *

with open("config.json") as f:
    config=json.load(f)

def gen_text(Texts):
    parsed_text=""
    for text in Texts:
        parsed_text+=MeCab.Tagger("-Owakati").parse(text)

    model=markovify.NewlineText(format_text(parsed_text),2)
    while True:
        text=model.make_sentence_with_start(beginning="厳しい")
        text=text.replace(" ","")
        if len(text)<=140:
            return text

def do_tweet(text):
    with open(config["API_Key_path"]) as f:
        API_key=json.load(f)
    
    consumer_key=API_key["consumer_key"]
    consumer_secret=API_key["consumer_secret"]
    access_token=API_key["access_token"]
    access_token_secret=API_key["access_token_secret"]
    
    auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api=tweepy.API(auth)

    api.update_status(text)

if __name__=="__main__":
    with open(config["text_path"]) as f:
        Texts=f.readlines()
    do_tweet(gen_text(Texts))