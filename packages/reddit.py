from praw import Reddit
from os import getenv
from threading import Thread
from time import sleep
from random import choice

reddit = Reddit(client_id = getenv('REDDIT_ID'),
                client_secret = getenv('REDDIT_SECRET'),
                user_agent = 'Nitrotype Bot')

class ImageFetcher:
    def __init__(self, subreddits={}, reload=60):
        auto_fetch = Thread(target=self.fetch, args=(subreddits, reload), daemon=True)
        auto_fetch.start()

    def fetch(self, subreddits={}, reload=60):
        media_types = ['.gif', '.png', '.jpg']

        while True:
            self.submissions = []
            for subreddit in subreddits:
                for submission in reddit.subreddit(subreddit).hot(limit=subreddits.get(subreddit)):
                    if submission.url[-4:] in media_types and 'i.redd.it' in submission.url:
                        self.submissions += [submission]
            sleep(reload)
        
    def image(self):
        try:
            submission = choice(self.submissions)
            return {'title' : submission.title,
                    'image' : submission.url,
                    'upvotes' : submission.score,
                    'comments' : submission.num_comments,
                    'url' : submission.shortlink}
        except:
            return