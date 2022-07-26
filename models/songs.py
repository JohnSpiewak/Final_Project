from mysqlconnection import connectToMySQL
from flask import flash
import json
db = 'songs_schema'


class Song:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.artist = data['artist']
        self.album = data['album']
        self.release_date = data['release_date']
        self.user_id = data['user_id']
        self.num_likes = data.get('num_likes')
        self.is_liked = bool(data['is_liked']) if 'is_liked' in data else None
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_song_details(cls, song_id):
        query = "SELECT s.*, u.first_name, u.last_name FROM songs s JOIN users u ON s.user_id = u.id WHERE s.id = %(song_id)s"
        results = connectToMySQL(db).query_db(query,{'song_id': song_id})
        print(results)
        return results[0]

    @classmethod
    def create_song(cls, data, user_id):
        print("I am creating a new show with", data)
        query = f"INSERT INTO songs (title, artist, album, release_date, user_id) values (%(title)s, %(artist)s, %(album)s, %(release_date)s, {user_id})"
        results = connectToMySQL(db).query_db(query,data)
        return results

    @classmethod
    def get_all_songs(cls, user_id):
        query = """
            SELECT songs.*, 
            COUNT(likes.user_id) AS num_likes, 
            CASE 
	            WHEN songs.id IN (SELECT l.song_id FROM likes l WHERE l.user_id = %(user_id)s) THEN 1 
	            ELSE 0 
            END AS is_liked 
            FROM songs 
            LEFT JOIN likes 
	            ON songs.id=likes.song_id 
            GROUP BY songs.id;"""
        data = {
            'user_id' : user_id
        }
        results = connectToMySQL(db).query_db(query, data)
        songs = []
        for song_dict in results:
            song = cls(song_dict)
            songs.append(song)
        return songs

    @classmethod
    def get_one_song(cls, data):
        query = "SELECT * FROM songs Where id = %(song_id)s;"
        results = connectToMySQL(db).query_db(query, data)
        song = cls(results[0])
        return song
    
    @classmethod
    def update_song(cls, data):
        print(data)
        query = "UPDATE songs SET title = %(title)s, artist = %(artist)s, album = %(album)s, release_date = %(release_date)s Where id = %(song_id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def delete_song(cls, song_id):
        query = f"DELETE FROM songs WHERE id = {song_id}"
        results = connectToMySQL(db).query_db(query)
        return results

    @classmethod
    def like_song(cls, user_id, song_id):
        data = {
            'user_id' : user_id, 
            'song_id' : song_id
        }
        query = "INSERT INTO likes (user_id, song_id) values (%(user_id)s, %(song_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @staticmethod
    def validate_song(song_info):
        print(song_info)
        is_valid = True
        if len(song_info['title']) < 3:
            flash('Song Title must be greater than 2 characters.')
            is_valid = False
        if len(song_info['album']) < 1:
            flash('Album Name must be greater than 0 characters.')
            is_valid = False
        if len(song_info['artist']) < 1:
            flash('Artist name must be greater than 0 characters.')
            is_valid = False
        return is_valid