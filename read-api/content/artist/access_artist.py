from requests import get
import json
import content.token.access_token as access_token


def search_for_artist(token, year, limit):
    url = "https://api.spotify.com/v1/search?"
    headers = access_token.get_auth_header(token)
    query = f"q=year:{year}&type=artist&limit=" + limit
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    return json_result
