import json
import os
import re
import mojimoji
import unicodedata
from urlextract import URLExtract
from xml.sax.saxutils import unescape

extractor=URLExtract()
with open("config.json") as f:
    config=json.load(f)

def format_text(t):
    t = t.replace('　', ' ')  # Full width spaces
    # t = re.sub(r'([。．！？…]+)', r'\1\n', t)  # \n after ！？
    t = re.sub(r'(.+。) (.+。)', r'\1 \2\n', t)
    t = re.sub(r'\n +', '\n', t)  # Spaces
    t = re.sub(r'([。．！？…])\n」', r'\1」 \n', t)  # \n before 」
    t = re.sub(r'\n +', '\n', t)  # Spaces
    t = re.sub(r'\n+', r'\n', t).rstrip('\n')  # Empty lines
    t = re.sub(r'\n +', '\n', t)  # Spaces
    return t

#完全なテキストのみにしてすべて全角文字に直して返す
def process_text(tweet):
    #手順
    # 1.URLを抜き取る(とりあえず半角文字をすべて取り出してそこからURLを抽出してreplaceする)
    # 2.メンションしてるアカウント名を除外
    # 3.HTMLの特殊文字をもとに戻す
    # 4.半角から全角に変換
    tweet=tweet.replace("\n","")#改行を除外

    #半角文字だけ抽出
    hankaku=[]
    for i in tweet:
        if unicodedata.east_asian_width(i)=="Na":
            hankaku.append(i)
        else:
            #全角文字のときに間を空けないとURLの検出ができない
            hankaku.append(" ")
    hankaku="".join(hankaku)
    #hankaku="".join([i for i in tweet if unicodedata.east_asian_width(i)=="Na"])
    urls=extractor.find_urls(hankaku)#URLを抽出
    hankaku=hankaku.split()
    mention_account=[i for i in hankaku if i[0]=="@"]#メンションしてるアカウントを抽出

    #1.URLを抜き取る
    for url in urls:
        tweet=tweet.replace(url,"")
    
    #2.メンションしてるアカウントを除外
    for ma in mention_account:
        tweet=tweet.replace(ma,"")
    
    #3.HTMLの特殊文字をもとに戻す
    tweet=unescape(tweet)
    
    #4.半角から全角に変換
    tweet=mojimoji.han_to_zen(tweet)
    tweet=format_text(tweet)
    return tweet

#jsonからツイートを読み取り, ツイートを要素とするリストにして返す
def get_tweet():
    path=config["data_path"]
    file_list=[os.path.join(path,i) for i in os.listdir(path) if ".json" in i]
    Tweets=[]

    for file in file_list:
        with open(file) as f:
            data_json=json.load(f)
        
        all_tweets=data_json["statuses"]
        for i in all_tweets:
            tweet=i["text"]
            if tweet[:2]!="RT":
                Tweets.append(process_text(tweet))
    return Tweets


if __name__=="__main__":
    with open(config["text_path"],"w") as f:
        f.writelines(get_tweet())
    print(len(get_tweet()))
