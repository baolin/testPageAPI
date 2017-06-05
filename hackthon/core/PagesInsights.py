from Posts import requests, json, query_api
from datetime import datetime

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

def getManagedPagesInsightsForOneUser(user_id, access_token):
    pages_info = getPagesForUser(user_id, access_token)
    print('pages_info')
    print(pages_info)
    pages_insights = {}
    for page_info in pages_info:
        page_access_token = page_info[0]
        page_id = page_info[1]
        page_insights = getInsightsForOnePage(page_id, page_access_token)
        if page_insights is not None:
            pages_insights[page_id] = page_insights
    return pages_insights

def getInsightsForOnePage(page_id, page_access_token):
    response = query_api(page_id, 'insights', page_access_token, metric='page_fan_adds_unique', period='week')
    if len(response) == 0:
        return None
    page_insights = response[0]['values']
    page_insights_with_modified_time = map(
        lambda v:
            (
                datetime.strptime(
                    v['end_time'][:-5],  # strip timezone
                    '%Y-%m-%dT%H:%M:%S',
                ).strftime('%Y/%m/%d'),
                v['value'],
            ),
        page_insights,
    )
    print((page_id, page_insights_with_modified_time))
    return page_insights_with_modified_time

if __name__ == '__main__':
    user_id = getUserIDFromUserAccessToken()
    # print user_id
    # print getPagesForUser(user_id)
    # print getManagedPagesInsightsForOneUser(user_id)
