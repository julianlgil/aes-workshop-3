import spotipy
import base64
from requests import post, get
import json
import Content.Token.access_token as access_token
import rabbitmq

def search_for_artist(token, year,limit,channel):
    url = "https://api.spotify.com/v1/search?"
    headers = access_token.get_auth_header(token)
    #query = f"q={artist_name}&type=artist&limit=" + limit
    query = f"q=year:{year}&type=artist&limit=" + limit
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    # print(len(json_result))
    message = str(json_result)
    rabbitmq.publisher(channel,message)
    # print("Send Artist")
    return json_result

def get_song_by_artist(token, artist_id, channel):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = access_token.get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content) ["tracks"]
    message = str(json_result)
    # rabbitmq.publisher(channel,message)
    return json_result