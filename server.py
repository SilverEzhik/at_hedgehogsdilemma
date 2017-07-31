from flask import Flask
import sys
import twitter
import re
from datetime import datetime

api = twitter.Api(consumer_key="",
                  consumer_secret="",
                  access_token_key="",
                  access_token_secret="")

username = sys.argv[1]

app = Flask(__name__)

@app.route('/')
def chrip():
    profile = api.GetUser(screen_name=username)

    if username is None:
        print("Username please")
        return 1

    pronoun = "They"

    if re.search("she/her", profile.description, re.IGNORECASE):
        pronoun = "She"
    elif re.search("he/him", profile.description, re.IGNORECASE):
        pronoun = "He"

    tweets = api.GetUserTimeline(screen_name=username)

    #good people use templates but we are not good people

    page = "<!DOCTYPE HTML><html><head><title>@" + username + "</title><style>html{transform-origin:top;transform:scale(1,1.5)}body{margin:0;background-color:#000;color:#fff}.chirp:nth-child(even){background-color:#070707}.chirp{width:100vw;height:50vh;padding-top:10vh;padding-bottom:15vh}.container{margin:0 auto;padding-bottom:20vh;width:80%;height:60vh}.username{height:60%;font-size:20vh;word-wrap:break-word;line-height:16vh}.episode{height:10%;font-family:sans-serif;font-size:5vh;font-weight:700}.tweet{height:30%;font-size:5vh}</style></head><body>"

    for tweet in tweets:
        page += "<div class=chirp><div class=container><div class=username>@" + tweet.user.screen_name + "</div><div class=episode>EPISODE:<span class=date>" + datetime.fromtimestamp(tweet.created_at_in_seconds).strftime('%Y%m%d') + "</span></div><div class=tweet><span class=pronoun>" + pronoun + "</span> said,\"<span class=tweet>" + tweet.text + "</span>\"</div></div></div>"

    page += "</body></html>"
    return page

if __name__ == '__main__':
    app.run()
