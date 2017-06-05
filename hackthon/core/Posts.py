"""Query Example."""

import requests
import json

#ACCESS_TOKEN = (
    #'EAACEdEose0cBAMrtx3REKZAWMninNwJIc1j9vRa05pfJf0kN7BVZBEVAHyLzyhaCTMVoneyBmJGt1uhZBhEWsFO5CA1QD8ZA3XiADUNgMdjetMiEqIPZAHkPQAp0IDPsK1GgyXAvWPlfuYrDNwAwqbkgip025aYTGO6VHu1UiqFWEcQOlQBUexs0deNT2CiZBX8ptyTgs8hwZDZD')
PAGE_ID = 1322842141107011
PREFIX = 'https://graph.facebook.com/v2.9'
PAGINATE_LIMIT = 25


def query_api(page_id, endpoint, access_token, **params):
    # always paginate with max limit, but capture provided limit
    # since api limit might be lower then the amount we want
    desired_limit = -1
    if 'limit' in params:
        desired_limit = params['limit']
        params['limit'] = PAGINATE_LIMIT
    param_strings = map(
        lambda (k, v): '{}={}'.format(k, v),
        params.iteritems()
    )
    param_strings.append('access_token={}'.format(access_token))
    param_string = '&'.join(param_strings)
    rurl = '{}/{}/{}?{}'.format(
        PREFIX,
        page_id,
        endpoint,
        param_string,
    )
    #print(rurl)

    response_data = list()
    while True:
        #  get and decode response
        response = requests.get(rurl)
        response = json.loads(response.content)
        if 'data' in response:
            if len(response['data']) == 0:
                return response_data
            response_data += response['data']

        if desired_limit != -1 and len(response_data) >= desired_limit:
            break

        #  get paging info to see if there is more data to fetch
        paging = None
        rurl = None
        if 'paging' in response:
            paging = response['paging']
            if 'next' in paging:
                rurl = paging['next']
        if rurl is None:
            break

    if desired_limit > 0:
        return response_data[:desired_limit]
    return response_data

def get_most_commented_posts(page_id):
    response = query_api(page_id, 'feed', fields='comments.summary(true)')
    #  get number of comments each post has
    posts_with_comments = list()
    for value in response:
        comment_count = 0
        if 'comments' in value:
            comment_count = value['comments']['summary']['total_count']
        posts_with_comments.append((value['id'], comment_count))
    posts_with_comments.sort(key=lambda x: x[1], reverse=True)
    return posts_with_comments


def get_most_liked_posts(page_id, access_token):
    response = query_api(page_id, 'feed', access_token, fields='likes.summary(true)')
    #  get number of likes each post has
    posts_with_likes = list()
    for value in response:
        likes = 0
        if 'likes' in value:
            likes = value['likes']['summary']['total_count']
        posts_with_likes.append((value['id'], likes))
    posts_with_likes.sort(key=lambda x: x[1], reverse=True)
    return posts_with_likes


def get_poster_frequency(page_id, access_token):
    response = query_api(page_id, 'feed', access_token, fields='from')
    poster_ids = map(
        lambda v: v['from']['id'],
        response,
    )
    frequencies = {}
    for poster_id in poster_ids:
        if poster_id not in frequencies:
            frequencies[poster_id] = 0
        frequencies[poster_id] += 1
    frequencies = frequencies.items()
    frequencies.sort(key=lambda x: x[1], reverse=True)
    return frequencies

if __name__ == '__main__':
    print get_most_commented_posts()
