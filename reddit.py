import pandas as pd
import praw
from praw.models import MoreComments
from dotenv import dotenv_values

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
for submission in subreddit.hot(limit=5):
    titles.append(submission.title)
    scores.append(submission.score)
    ids.append(submission.id)
    comments.append(submission.comments)

# inserting data into dataframe
df['Title'] = titles
df['Upvotes'] = scores
df['Id'] = ids
df['Comments'] = comments

print(df.shape)
print(df.head(10))

# get comments from a certain submission
for top_level_comment in df['Comments'][1]:
    if isinstance(top_level_comment, MoreComments):
        continue
    print(top_level_comment.body)
