from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField, DateField, FileField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

# Create a Form Class
class UserForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	username = StringField("Username", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	favorite_color = StringField("Favorite Color")
	password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
	password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
	profile_pic = FileField("Profile Pic")
	submit = SubmitField("Submit")

#Create new song
class SongForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	artist = StringField("Artist", validators=[DataRequired()])
	album = StringField("Album", validators=[DataRequired()])
	genre = StringField("Genre", validators=[DataRequired()])
	release_date = DateField("Release Date", format='%Y-%m-%d', validators=[DataRequired()])
	song_file = FileField("Song File", validators=[DataRequired()])
	song_profile = FileField("Song Image")
	submit = SubmitField("Submit")

#Create new Playlist
class PlaylistForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	description = StringField("Description", validators=[DataRequired()])
	playlist_profile = FileField("Image")
	