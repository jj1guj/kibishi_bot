import markovify
import MeCab
import json
from markovify import text
import tweepy
from read_data import *

with open("/home/jj1guj/kibishi_bot/config.json") as f:
    config=json.load(f)

def train(Texts):
    parsed_text=""
    for text in Texts:
        parsed_text+=MeCab.Tagger("-Owakati").parse(text)

    model=markovify.NewlineText(format_text(parsed_text),2)
    model_json=model.to_json()

    with open(config["model_path"],"w") as f:
        f.write(model_json)


if __name__=="__main__":
    train(get_tweet())