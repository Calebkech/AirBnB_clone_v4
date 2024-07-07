import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Song table
class Song(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100), nullable=True)
    genre = db.Column(db.String(50), nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    song_file = db.Column(db.String(255), nullable=False)
    song_profile = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Song {self.title}>"

# User table
class Users(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    profile_pic = db.Column(db.String(255), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_creater = db.Column(db.Boolean, default=False)
    playlists = db.relationship('Playlist', back_populates='user', cascade='all, delete-orphan')

    # Do some password stuff!
    password_hash = db.Column(db.String(256))

    def __repr__(self):
        return f"<User {self.username}>"

# Playlist table
class Playlist(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    playlist_profile = db.Column(db.String(255), nullable=True)
    songs = db.relationship('Song', secondary='playlist_song', backref='playlists')
    user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete="CASCADE"))
    user = db.relationship('Users', back_populates='playlists')

    def __repr__(self):
        return f"<Playlist {self.name}>"

# Association table for the many-to-many relationship between Playlist and Song
playlist_song = db.Table('playlist_song',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True),
    db.Column('song_id', db.String(36), db.ForeignKey('song.id'), primary_key=True)
)
