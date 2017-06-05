from Posts import requests, json, query_api, get_most_liked_posts
from PagesInsights import getManagedPagesInsightsForOneUser

#page_id = 1322842141107011
PREFIX = 'https://graph.facebook.com/v2.9'
#ACCESS_TOKEN = ("EAACEdEose0cBAMrtx3REKZAWMninNwJIc1j9vRa05pfJf0kN7BVZBEVAHyLzyhaCTMVoneyBmJGt1uhZBhEWsFO5CA1QD8ZA3XiADUNgMdjetMiEqIPZAHkPQAp0IDPsK1GgyXAvWPlfuYrDNwAwqbkgip025aYTGO6VHu1UiqFWEcQOlQBUexs0deNT2CiZBX8ptyTgs8hwZDZD"
#)

def getUserIDFromUserAccessToken(access_token):
    rurl = PREFIX + '/me?access_token&fields=id&access_token=' + access_token
    response = requests.get(rurl)
    response = json.loads(response.content)
    id = response['id']
    return id

def getPagesForUser(user_id, access_token):
    response = query_api(user_id, 'accounts', access_token)
    pages_info = map(
        lambda v: (v['access_token'],v['id']),
        response,
    )
    return pages_info

def get_aggregated_insights_cross_pages(user_id, access_token):
    return getManagedPagesInsightsForOneUser(user_id, access_token)

def get_aggregated_top_n(user_id, access_token):
    pages_info = getPagesForUser(user_id, access_token)
    cross_pages_result = {}
    for page_info in pages_info:
        result = get_most_liked_posts(page_info[1], page_info[0])
        cross_pages_result.update(result[:10])
    cross_pages_result = cross_pages_result.items()
    cross_pages_result.sort(key=lambda x: x[1], reverse=True)
    return cross_pages_result[:10]

if __name__ == '__main__':
    user_id = getUserIDFromUserAccessToken()
    print get_aggregated_top_n(user_id)
    print get_aggregated_insights_cross_pages(user_id)
