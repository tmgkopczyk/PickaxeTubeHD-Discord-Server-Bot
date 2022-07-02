import requests
api_key = "AIzaSyCYU-_HGzv6g5B7_P4Gm0-CRVk1hppBBIs"


def get_profile_info(channel_id):
    params = {
        "part":['snippet','contentDetails','statistics'],
        "id":channel_id,
        "key":api_key
    }
    response = requests.get("https://youtube.googleapis.com/youtube/v3/channels",params=params).json()
    return response['items'][0]['snippet']


def get_channel_playlists(channel_id):
    params = {
        "part":['snippet','contentDetails','statistics'],
        "id":channel_id,
        "key":api_key
    }
    response = requests.get("https://youtube.googleapis.com/youtube/v3/channels",params=params).json()
    return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

def get_video_id(playlist_id):
    params = {
        "part":['snippet','contentDetails'],
        "playlistId":playlist_id,
        "key":api_key
    }
    response = requests.get("https://youtube.googleapis.com/youtube/v3/playlistItems",params=params).json()
    latest_video = response['items'][0]['contentDetails']['videoId']
    return latest_video

def get_video_info(video_id):
    params = {
        "part":['snippet','contentDetails','statistics'],
        "id":video_id,
        "key":api_key
    }
    response = requests.get("https://youtube.googleapis.com/youtube/v3/videos",params=params).json()
    return response['items'][0]


