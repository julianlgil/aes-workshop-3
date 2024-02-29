import json
from typing import Dict, List
import psycopg2
import atexit

from utils.utils import RabbitMQ
import time
import os


class DB:
    def __init__(self):
        db_port = os.getenv('POSTGRES_PORT')
        db_user = os.getenv('POSTGRES_USER')
        db_name = os.getenv('POSTGRES_DB')
        db_password = os.getenv('POSTGRES_PASSWORD')
        db_host = "db"

        self.conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                database=db_name
        )

        #Le cursor
        self.cursor = self.conn.cursor()

        self.initialize_db()


    #Creo la tabla si no existe
    def initialize_db(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS spotify_metrics (
            id SERIAL PRIMARY KEY,
            artist_quantity INTEGER,
            genre VARCHAR(255),
            avg_popularity FLOAT
        );
        """)

        self.conn.commit()

    #Cerrar DB connection
    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    #Funcion principal
    def save_data(self, filtered_data) -> bool:
        try:
            print("Empiezo save data")
            #Si el elemento existe, re calcule, sino, creelo
            for genre, artist_elmnt in filtered_data.items():
                genreExists = self.genre_exists(genre)
                print(f"EXISTE GENERO? {genreExists}")

                if len(artist_elmnt) == 1:
                    continue
                
                if genreExists:
                    current_artist_quantity, current_avg_popularity = self.get_genre_stats(genre)

                    new_artist_quantity = current_artist_quantity + len(artist_elmnt)
                    new_avg_popularity = round(((current_artist_quantity * current_avg_popularity) +
                                          sum(artist["popularity"] for artist in artist_elmnt)) / new_artist_quantity,2)


                    self.cursor.execute("""
                        UPDATE spotify_metrics
                        SET artist_quantity = %s, avg_popularity = %s
                        WHERE genre = %s;
                    """, (new_artist_quantity, new_avg_popularity, genre))
                else:
                    artist_quantity = len(artist_elmnt)
                    avg_popularity = sum(artist["popularity"] for artist in artist_elmnt) / artist_quantity

                    self.cursor.execute("""
                        INSERT INTO spotify_metrics (artist_quantity, genre, avg_popularity)
                        VALUES (%s, %s, %s);
                    """, (artist_quantity, genre, round(avg_popularity, 2)))

                    print(f"Genero '{genre}' con {artist_quantity} artistas y popu promedio de {avg_popularity}")
            
            #Commit y finite
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error guardando esta joda: {e}")
            return False
    
    #Verificar si genero existe
    def genre_exists(self, genre):
        self.cursor.execute("SELECT COUNT(*) FROM spotify_metrics WHERE genre = %s;", (genre,))
        count = self.cursor.fetchone()[0]
        return count > 0
    
    #Trae valores actuales de popularitdad y cantidad artistas
    def get_genre_stats(self, genre):
        self.cursor.execute("SELECT artist_quantity, avg_popularity FROM spotify_metrics WHERE genre = %s;", (genre,))
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            return 0, 0.0




class RabbitCallbackDB:
    def __init__(self, rabbit: RabbitMQ, db: DB) -> None:
        self.rabbit = rabbit
        self.db = db

    def getRabbitData(self, ch, method, properties, body):
        source = body.decode('utf-8')

        source=json.loads(source)

        time.sleep(2)
        ch.basic_ack(delivery_tag=method.delivery_tag)

        print(f"source is this {source}")
        print("This is before the db idea")
        if self.db.save_data(source):
            print("Exito")
        else: 
            print("Error guardando datos")

        time.sleep(2)


if __name__ == '__main__':
    rabbit = RabbitMQ(amqp_url=os.environ['AMQP_URL'])
    db_source_queue = os.getenv('FILTER_QUEUE_NAME')

    #DB 
    db = DB()

    #Trae el queue de rabbit devuelve objeto
    source = rabbit.subscribe(db_source_queue, RabbitCallbackDB(rabbit, db).getRabbitData)

    #Siempre corre al cerrar
    atexit.register(db.close_connection)