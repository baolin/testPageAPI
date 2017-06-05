"""Analyze sentiment of visitor posts for page."""

import requests
import pprint
import json
from Posts import query_api
from Posts import PAGE_ID

SA_URL = 'http://text-processing.com/api/sentiment/'


def visitor_posts_sentiment(page_id):
    """Get post ids, messaged and sentiment rating."""
    response = query_api(
        page_id,
        'feed',
        fields='id,created_time,message,from',
    )
    sentiment = {}
    for post in response:
        #  filter out posts from the page itself
        if 'from' in post:
            poster_id = post['from']['id']
            if poster_id == str(page_id):
                continue

        sentiment[post['id']] = {}
        if 'message' in post:
            message = post['message']
            sa = requests.post(SA_URL, data={'text': message})
            sa = json.loads(sa.content)
            sentiment[post['id']] = {
                'message': message,
                'rating': sa['label'],
            }
    return sentiment

if __name__ == '__main__':
    r = visitor_posts_sentiment(PAGE_ID)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(r)
