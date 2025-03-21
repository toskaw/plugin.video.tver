import requests

from lib import get_random_ua, get_custom_img_path, localize, log

URL_TOKEN_SERVICE = 'https://platform-api.tver.jp/v2/api/platform_users/browser/create'
URL_TAG_SEARCH_WS = 'https://platform-api.tver.jp/service/api/v1/callTagSearch/{}'
URL_LIST_EPISODES =  URL_TAG_SEARCH_WS + '?platform_uid={}&platform_token={}'
URL_VIDEO_WEBSITE = 'https://tver.jp/{}s/{}'
URL_VIDEO_PICTURE = 'https://statics.tver.jp/images/content/thumbnail/{}/small/{}.jpg'
URL_VIDEO_CONTENT = 'https://statics.tver.jp/content/{}/{}.json'
URL_VIDEO_INFO    = 'https://platform-api.tver.jp/service/api/v1/callEpisode/{}'
URL_LIST_INFO     =  URL_VIDEO_INFO + '?platform_uid={}&platform_token={}'
URL_SEASONS_INFO  =  'https://platform-api.tver.jp/service/api/v1/callSeasonEpisodes/{}' + '?platform_uid={}&platform_token={}'

CATEGORIES = [
        ("variety",localize(30005), get_custom_img_path("variety.jpg")),
        ("drama",localize(30006), get_custom_img_path("drama.jpg")),
        ("anime",localize(30007), get_custom_img_path("anime.jpg")),
        ("documentary",localize(30008), get_custom_img_path("documentary.jpg")),
        ("sports",localize(30009), get_custom_img_path("sports.jpg")),
        ("other",localize(30010), get_custom_img_path("others.jpg")),
    ]
TAGS = ["variety", "drama", "anime", "documentary", "sports", "other" ]

def get_categories():
    return CATEGORIES

def fetch_api_token():
    resp = requests.post(URL_TOKEN_SERVICE, data=b'device_type=pc', headers={
                'user-agent': get_random_ua(),
                'Origin': 'https://s.tver.jp',
                'Referer': 'https://s.tver.jp/',
                'Content-Type': 'application/x-www-form-urlencoded',
            }, timeout=10)
    
    json_token = resp.json()

    uid = json_token['result']['platform_uid']
    token = json_token['result']['platform_token']
    return (uid,token)

def fetch_episodes(category):
    data = None
    if category in TAGS:
        (uid, token) = fetch_api_token()
        resp = requests.get(URL_LIST_EPISODES.format(category, uid, token), headers={'x-tver-platform-type': 'web'}, timeout=10)
        data = resp.json()
    else:
        data = fetch_episodes_season(category)
    return data

def fetch_episode(id):
    (uid, token) = fetch_api_token()
    resp = requests.get(URL_LIST_INFO.format(id, uid, token), headers={'x-tver-platform-type': 'web'}, timeout=10)
    data = resp.json()

    return data
def fetch_episodes_season(season):
    (uid, token) = fetch_api_token()
    resp = requests.get(URL_SEASONS_INFO.format(season, uid, token), headers={'x-tver-platform-type': 'web'}, timeout=10)
    data = resp.json()

    return data
    
