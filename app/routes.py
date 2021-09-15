from flask import render_template, request
from werkzeug.utils import send_from_directory
from app import app
from app import analysisFunctions
import tweepy
import wordcloud
import shutil

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_tweets():
    twitter_handle = request.form['twitter_handle']

    api_key = "INSERT TWITTER API KEY"
    api_key_secret = "INSERT TWITTER API KEY SECRET"

    access_token = "INSERT TWITTER API ACCESS TOKEN"
    access_token_secret = "INSERT TWITTER API ACCESS TOKEN SECRET"

    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweet_limit = 130
    tweets = []
    likes = []
    retweets = []

    #Parse tweets, remove retweets, populate tweets, likes, and retweets
    for tweet in tweepy.Cursor(api.user_timeline, id = twitter_handle, tweet_mode = 'extended').items(tweet_limit):
        if len(tweets) < 100:
            if 'RT' not in tweet.full_text:
                tweets.append(tweet.full_text)
                likes.append(tweet.favorite_count)
                retweets.append(tweet.retweet_count)

    #Build Wordcloud
    alphabet = ["a",'b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    additions = ["or", "and", "but", "https","co",'nhttps']
    wordcloud.STOPWORDS.update(alphabet, additions)
    cloud = wordcloud.WordCloud(max_words=50, width=500, height=500, background_color="black", colormap="inferno")
    cloud.generate(str(tweets))
    cloud.to_file('image.png')
    source = "image.png"
    destination = 'app/static'
    shutil.copy(source,destination)

    #Run analysis functions
    avg_likes = round(analysisFunctions.avg_likes(likes), 2)
    avg_retweets = round(analysisFunctions.avg_RT(retweets), 2)
    avg_words = round(analysisFunctions.tweet_wordavg(tweets), 2)
    avg_chars = round(analysisFunctions.tweet_charavg(tweets), 2)
    avg_polarity = round(analysisFunctions.polarity_analysis(tweets), 2)
    avg_subjectivity = round(analysisFunctions.subjectivity_analysis(tweets), 2)
    fkgl_score = round(analysisFunctions.fkgl_analysis(tweets), 2)
    smog_score = round(analysisFunctions.smog_analysis(tweets),2 )

    return render_template('results.html', avgLikes = avg_likes, avgRetweets = avg_retweets, avgWords = avg_words, avgChars = avg_chars, avgPolarity = avg_polarity,
        avgSubjectivity = avg_subjectivity, fkglScore = fkgl_score, smogScore = smog_score)