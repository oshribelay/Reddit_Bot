import pandas as pd
import praw
from praw.models import MoreComments
from dotenv import dotenv_values
from tts import text_to_speech
from mutagen.mp3 import MP3


def initialize_subreddit_object():
    # parse .env file
    config = dotenv_values("../.env")
    # print(config.values())

    # define user_agent
    user_agent = "python-reddit-bot"

    # creating reddit object
    reddit = praw.Reddit(client_id=config['REDDIT_ID'],
                         client_secret=config['REDDIT_SECRET'],
                         user_agent=user_agent)

    # define subreddit
    subreddit_name = "AskReddit"
    subreddit = reddit.subreddit(subreddit_name)
    print(subreddit.display_name)
    return subreddit


def get_data_from_subreddit(subreddit_object):

    df = pd.DataFrame()  # create empty dataframe to store data from subreddit

    # empty lists to store data from api call
    titles = []
    scores = []
    ids = []
    comments = []

    # looping through subreddit and scraping the data
    for submission in subreddit_object.hot(limit=2):
        titles.append(submission.title)
        scores.append(submission.score)
        ids.append(submission.id)
        comments.append(submission.comments.list())

    # inserting data into dataframe
    df['Title'] = titles
    df['Upvotes'] = scores
    df['Id'] = ids
    df['Comments'] = comments

    print(df.shape)
    print(df.head(2))

    # get comments from a certain submission
    comments_array = []
    for idx, top_level_comment in enumerate(comments[1]):
        if isinstance(top_level_comment, MoreComments):
            continue
        comments_array.append((idx, top_level_comment.body))

    return [df, comments_array]


# saving all the comments as audio files no more than 50 secs which is the limit that tik-tok allows
def convert_comments_to_audio(comments_arr):

    length = 0
    for index, comment in comments_arr:
        if length <= 50:
            text_to_speech(comment, is_comment=True, comment_id=index)
            print(f"saved comment {index+1}")
            audio = MP3(f"../audio_files/comment {index}.mp3")
            length_sec = audio.info.length
            length += length_sec
        else:
            return index


def convert_title_to_audio(title):
    text_to_speech(title, is_comment=False)
    print("saved title successfully")
