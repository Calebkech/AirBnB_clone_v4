import os
import uuid
from datetime import datetime
from flask import request, redirect, url_for, render_template, flash, current_app, Blueprint
from werkzeug.utils import secure_filename
from .models import db, Song, Users, Playlist
from flask import abort
from .forms import UserForm, SongForm, LoginForm, PlaylistForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_login import login_required


main = Blueprint('main', __name__)



@main.route('/')
@login_required
def index():
    sample_playlists = [
        {'name': 'Chill Hits', 'description': 'Relax and unwind with these chill hits.', 'song_count': 20},
        {'name': 'Workout Mix', 'description': 'Get pumped with this energetic workout playlist.', 'song_count': 30},
        {'name': 'Top 50', 'description': 'The top 50 songs right now.', 'song_count': 50},
    ]
    return render_template('index.html', playlists=sample_playlists)


@main.route('/song/song_list')
@login_required
def songs():
    songs = Song.query.all()
    return render_template('songs.html', songs=songs)

@main.route('/song/add_songs', methods=['GET', 'POST'])
@login_required
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
            profile_file_path = None

            if song_file:
                song_filename = secure_filename(song_file.filename)
                song_file_path = os.path.join('music', song_filename)  # Save relative path
                song_full_path = os.path.join(current_app.root_path, 'static', song_file_path)
                song_file.save(song_full_path)
                print(f"Song file saved to: {song_full_path}")

            if song_profile:
                profile_filename = secure_filename(song_profile.filename)
                profile_file_path = os.path.join('song_image', profile_filename)  # Relative path, no 'static/'
                image_full_path = os.path.join(current_app.root_path, 'static', profile_file_path)
                song_profile.save(image_full_path)
                print(f"Profile image saved to: {image_full_path}")
            else:
                profile_file_path = 'song_image/default_song_image.png'
                print("Using default profile image")

            # Create a new Song object
            new_song = Song(
                title=title,
                artist=artist,
                album=album,
                genre=genre,
                release_date=release_date,
                song_file=song_file_path,  # Save relative path in DB
                song_profile=profile_file_path  # Save relative path in DB
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

@main.route('/playlist/playlist_list')
@login_required
def playlist():
    playlists = Playlist.query.all()
    return render_template('playlist.html', playlists=playlists)

@main.route('/playlist/add_playlist', methods=['GET', 'POST'])
@login_required
def add_playlist():
    form = PlaylistForm()
    if form.validate_on_submit():
        try:
            name = form.name.data
            description = form.description.data
            playlist_profile = form.playlist_profile.data

            #handle file upload
            playlist_profile = None
            playlist_profile_file_path = ""

            if playlist_profile:
                playlist_profile = secure_filename(playlist_profile.filename)
                playlist_profile_file_path = os.path.join('playlist', playlist_profile)
                image_full_path = os.path.join(current_app.root_path, 'static', playlist_profile_file_path)
                playlist_profile.save(image_full_path)
                print(f"Profile image saved to: {image_full_path}")
            else:
                playlist_profile = 'song_image/default_song_image.png'
                print(f"Profile image saved to: {playlist_profile}")
            
            #create new playlist Object
            new_playlist = Playlist(
                name=name,
                description=description,
                playlist_profile=playlist_profile_file_path
            )

            #add playlist object to the database
            db.session.add(new_playlist)
            db.session.commit()
            flash('Playlist Created Successfully!')
            return redirect(url_for('main.playlist'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error Occured while creating the Playlist: {str(e)}')
    return render_template('add_playlist.html', form=form)

@main.route('/song/delete_song/<string:song_id>', methods=['POST'])
@login_required
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
@login_required
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
                flash("Registration Successfully!")
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
@login_required
def users():
    users = Users.query.order_by(Users.date_added).all()
    return render_template("user_list.html", users=users)

@main.route('/user/update/<string:user_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
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


@main.route('/admin')
def admin_page():
    return render_template('admin.html')
