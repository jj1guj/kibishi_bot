import markovify
import MeCab
import json
from markovify import text
import slackweb
import time
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
    start=time.time()
    train(get_tweet())
    end=time.time()

    #学習が終わったらTwitterで通知
    with open(config["Slack_Webhook_path"]) as f:
        j=json.load(f)
    webhook_url=j["url"]
    slack=slackweb.Slack(url=webhook_url)
    slack.notify(text="train completed!\nelapsed {:.2f} sec".format(end-start),username="Kibishi bot",icon_url="http://pbs.twimg.com/profile_images/1461228468277215232/L4WiX6xa_400x400.jpg")