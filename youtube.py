import requests
api_key = "AIzaSyDY9NziRx7HW8Fw6b5JiAmUlan2_LgF1Dg"
def get_channel_info():
  response = requests.get("https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id=UCHMXHaWoFTa4FRsm7aLaUbQ&key={}".format(api_key)).json()
  return response['items'][0]['snippet']['thumbnails']['high']['url']

def get_upload_playlist():
  response = requests.get("https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id=UCHMXHaWoFTa4FRsm7aLaUbQ&key={}".format(api_key)).json()
  return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

def get_video_id(playlist_id):
  response = requests.get("https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&playlistId={}&key={}".format(playlist_id,api_key)).json()
  return response['items'][0]['contentDetails']['videoId']
  
def get_video_info(video_id):
  response = requests.get("https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id={}&key={}".format(video_id,api_key)).json()
  return response['items'][0]['snippet'],response['items'][0]['statistics']

profile_image = get_channel_info()
upload_playlist = get_upload_playlist()
videos = get_video_id(upload_playlist)
video_info = get_video_info(videos)
video_stats = video_info[1]
video_info = video_info[0]