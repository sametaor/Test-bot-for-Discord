import praw
import os
from dotenv import load_dotenv

load_dotenv('token.env')

reddit = praw.Reddit(client_id=os.getenv('PRAW_CLIENT_ID'), client_secret=os.getenv('PRAW_CLIENT_SECRET'), username="PRAW_USERNAME", password=os.getenv('PRAW_PASSWORD'), user_agent=os.getenv('PRAW_USER_AGENT'), check_for_async=False)

