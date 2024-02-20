import spotipy
import json
import Content.Token.access_token as access_token
import Content.Artist.access_artist as access_artist
import properties
import Content.Artist.random_year as random_year
import rabbitmq

def process_loop(token, artists):
    #print(artists[0]["id"])
    #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    for i in artists:
        artist_id =i["id"]
        # print(i["name"] + " : " + artist_id)
        songs = access_artist.get_song_by_artist(token,artist_id,channel)
        # print(len(songs))

token = access_token.get_token()
connection,channel = rabbitmq.open_connection()

for i in range(properties.random_year_quantity):
    year=random_year.random_year()
    print(str(i) + " : " + str(year))
    artists = access_artist.search_for_artist(token, year,properties.limit,channel)
    process_loop(token, artists)

rabbitmq.close_connection(connection)


