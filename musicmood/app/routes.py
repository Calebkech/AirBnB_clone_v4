import os
import uuid
from datetime import datetime
from flask import request, redirect, url_for, render_template, flash, current_app, Blueprint
from werkzeug.utils import secure_filename
from .models import db, Song, Users
from flask import abort
from .forms import UserForm, SongForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

main = Blueprint('main', __name__)

@main.route('/')
def index():
    sample_playlists = [
        {'name': 'Chill Hits', 'description': 'Relax and unwind with these chill hits.', 'song_count': 20},
        {'name': 'Workout Mix', 'description': 'Get pumped with this energetic workout playlist.', 'song_count': 30},
        {'name': 'Top 50', 'description': 'The top 50 songs right now.', 'song_count': 50},
    ]
    return render_template('index.html', playlists=sample_playlists)

@main.route('/song/song_list')
def songs():
    songs = Song.query.all()
    return render_template('songs.html', songs=songs)

@main.route('/song/add_songs', methods=['GET', 'POST'])
def add_songs():
    form = SongForm()
    if form.validate_on_submit():
        try:
            title = form.title.data
            artist = form.artist.data
            album = form.album.data
            genre = form.genre.data
            release_date = form.release_date.data

            # Handle file upload
            song_profile = form.song_profile.data
            song_file = form.song_file.data

            song_file_path = None
            image_file_path = None

            if song_file:
                song_filename = secure_filename(song_file.filename)
                song_file_path = os.path.join('static/music', song_filename)  # Save relative path
                song_full_path = os.path.join(current_app.root_path, song_file_path)
                song_file.save(song_full_path)

            if song_profile:
                profile_filename = secure_filename(song_profile.filename)
                profile_file_path = os.path.join('static/song_image', profile_filename)
                image_full_path = os.path.join(current_app.root_path, profile_file_path)
                song_profile.save(image_full_path)
            else:
                # Set the default image path
                profile_filename = 'static/song_image/default_song_image.png'

            # Create a new Song object
            new_song = Song(
                title=title,
                artist=artist,
                album=album,
                genre=genre,
                release_date=release_date,
                song_file=song_file_path,  # Save relative path in DB
                song_profile=image_file_path
            )

            # Add the new song to the database
            db.session.add(new_song)
            db.session.commit()
            flash('Song added successfully!')
            return redirect(url_for('main.songs'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while adding the song: {str(e)}')
    
    return render_template('add_songs.html', form=form)

""" @main.route('/add_song', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        album = request.form['album']
        genre = request.form['genre']
        release_date = request.form['release_date']
        
        # Convert release_date to datetime object
        release_date = datetime.strptime(release_date, '%Y-%m-%d').date() if release_date else None

        # Handle file upload
        if 'song_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['song_file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join('static/music', filename)  # Save relative path
            full_path = os.path.join(current_app.root_path, file_path)
            file.save(full_path)
            
            # Create a new Song object
            new_song = Song(
                title=title,
                artist=artist,
                album=album,
                genre=genre,
                release_date=release_date,
                song_file=file_path  # Save relative path in DB
            )

            # Add the new song to the database
            db.session.add(new_song)
            db.session.commit()
            flash('Song added successfully!')
            return redirect(url_for('main.songs'))  # Redirect to the homepage after adding the song

    return render_template('add_song.html')"""

@main.route('/playlist/playlist_list')
def playlist():
    sample_playlists = [
        {'name': 'Chill Hits', 'description': 'Relax and unwind with these chill hits.', 'song_count': 20},
        {'name': 'Workout Mix', 'description': 'Get pumped with this energetic workout playlist.', 'song_count': 30},
        {'name': 'Top 50', 'description': 'The top 50 songs right now.', 'song_count': 50},
        {'name': 'Chill Hits', 'description': 'Relax and unwind with these chill hits.', 'song_count': 20},
        {'name': 'Workout Mix', 'description': 'Get pumped with this energetic workout playlist.', 'song_count': 30},
        {'name': 'Top 50', 'description': 'The top 50 songs right now.', 'song_count': 50},
        {'name': 'Chill Hits', 'description': 'Relax and unwind with these chill hits.', 'song_count': 20},
        {'name': 'Workout Mix', 'description': 'Get pumped with this energetic workout playlist.', 'song_count': 30},
        {'name': 'Top 50', 'description': 'The top 50 songs right now.', 'song_count': 50},
    ]
    return render_template('playlist.html', playlists=sample_playlists)

@main.route('/playlist/add_playlist', methods=['GET', 'POST'])
def add_playlist():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        cover_image = request.files.get('cover_image')
        # Handle saving the new playlist and the cover image here
        # For now, just redirect back to the playlists page
        return redirect(url_for('main.playlist'))
    return render_template('add_playlist.html')

@main.route('/song/delete_song/<string:song_id>', methods=['POST'])
def delete_song(song_id):
    #query the song to be deleted
    song = Song.query.get(song_id)

    #check if the song exitst
    if song:
        #if it exists delete
        db.session.delete(song)
        db.session.commit()
        flash('Song deleted successfully!', 'success')
    else:
        flash('Song not found!', 'error')
    
    #redirect back to song list
    return redirect(url_for('main.songs'))

@main.route('/song/update_song/<string:song_id>', methods=['GET', 'POST'])
def update_song(song_id):
    song = Song.query.get_or_404(song_id)
    form = SongForm(obj=song)  # Populate form fields with existing data

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                # Update only the fields that were submitted in the form
                form.populate_obj(song)

                # Handle file upload
                song_file = request.files.get('song_file')
                if song_file:
                    filename = secure_filename(song_file.filename)
                    file_path = os.path.join('static/music', filename)
                    full_path = os.path.join(main.root_path, file_path)
                    song_file.save(full_path)
                    song.file_path = file_path  # Save relative path in database

                # Update song details in the database
                db.session.commit()
                flash('Song updated successfully!', 'success')
                return redirect(url_for('main.songs'))

            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred while updating the song: {str(e)}', 'danger')

    return render_template('update_song.html', song=song, form=form)


@main.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        username = Users.query.filter_by(username=form.username.data).first()
        print(f'user: {user}, Username: {username}')
        if user is None and username is None:
            # Hash the password
            hashed_pw = generate_password_hash(form.password_hash.data, method='pbkdf2:sha256')
            user = Users(
                id=str(uuid.uuid4()),
                username=form.username.data,
                name=form.name.data,
                email=form.email.data,
                favorite_color=form.favorite_color.data,
                date_added=datetime.utcnow(), 
                password_hash=hashed_pw
            )

            db.session.add(user)
            try:
                db.session.commit()
                flash("User Added Successfully!")
                return redirect(url_for('main.users'))
            except IntegrityError as e:
                db.session.rollback()
                flash(f"An error occurred: {e.orig}")
        else:
            if user:
                flash("Email already exists!")
            if username:
                message = f'"Username already exists!"'
                flash(message)

        # Reset the form fields
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''

    our_users = Users.query.order_by(Users.date_added).all()
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

@main.route('/user/user_list')
def users():
    users = Users.query.order_by(Users.date_added).all()
    return render_template("user_list.html", users=users)

@main.route('/user/update/<string:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    user = Users.query.get_or_404(user_id)
    form = UserForm(obj=user)

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                
                form.populate_obj(user)

                #update user details
                db.session.commit()
                flash('User updated successfully!', 'success')
                return redirect(url_for('main.users'))
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred while updating the user: {str(e)}', 'danger')
    return render_template('update_user.html', user=user, form=form)

@main.route('/user/delete_user/<string:user_id>', methods=['POST'])
def delete_user(user_id):
    #query the user to be deleted
    user = Users.query.get(user_id)
    try:
        #check if the user exitst
        if user:
            #if it exists delete
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully!', 'success')
        else:
            flash('User not found!', 'error')
    except IntegrityError as e:
        db.session.rollback()
        flash(f"An error occored: {e.orig}")
    
    #redirect back to song list
    return redirect(url_for('main.users'))