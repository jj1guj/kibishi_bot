import markovify
import MeCab
import json
from read_data import *

with open("config.json") as f:
    config=json.load(f)

with open(config["text_path"]) as f:
    Texts=f.readlines()

parsed_text=""
for text in Texts:
    parsed_text+=MeCab.Tagger("-Owakati").parse(text)

#print(format_text(parsed_text))
model=markovify.NewlineText(format_text(parsed_text),2)
while True:
    text=model.make_sentence_with_start(beginning="厳しい")
    text=text.replace(" ","")
    if len(text)<=140:
        print(text,len(text))
        break