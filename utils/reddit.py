import pandas as pd
import praw
from praw.models import MoreComments
from dotenv import dotenv_values
from tts import text_to_speech
from mutagen.mp3 import MP3

# parse .env file
config = dotenv_values(".env")
print(config)

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


df = pd.DataFrame()  # create empty dataframe to store data from subreddit

# empty lists to store data from api call
titles = []
scores = []
ids = []
comments = []

# looping through subreddit and scraping the data
for submission in subreddit.hot(limit=2):
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

# saving all the comments as audio files no more than 50 secs which is the limit that tik-tok allows
length = 0
for idx, comment in comments_array:
    if length <= 50:
        text_to_speech(comment, is_comment=True, comment_id=idx)
        print(f"saved comment {idx}")
        audio = MP3(f"./audio_files/comment {idx}.mp3")
        length_sec = audio.info.length
        length += length_sec
    else:
        break
