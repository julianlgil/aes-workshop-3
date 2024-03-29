import base64
from requests import post
import json
import os

def get_token():
    auth_string = os.environ['CLIENT_ID'] + ":" + os.environ['CLIENT_SECRET']
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    print(token)
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}