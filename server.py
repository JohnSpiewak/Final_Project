from flask import Flask, render_template, redirect, request, flash, session
from models.users import User
from models.songs import Song
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
Flask.secret_key = "thisisasecret"

@app.route("/")
def registration():
    # users = User.get_all_users()
    return render_template("LoginReg.html")

@app.route("/add_user")
def add_user_page():
    return render_template("add_user.html")

@app.route("/create_user", methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name" : request.form['first_name'], 
        "last_name" : request.form['last_name'], 
        "email" : request.form['email'], 
        "password" : pw_hash,
    }

    session['user_id'] = User.create_user(data)
    return redirect("/home")

@app.route('/login_user', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')

    session['user_id'] = user.id
    return redirect('/home')

@app.route('/home')
def home():
    print(session)
    if "user_id" not in session:
        return redirect("/")
    user_id = session['user_id']
    data = {
        'user_id' : user_id
    }
    user = User.get_one_user(data)
    songs = Song.get_all_songs(user_id)
    print(user, songs)
    return render_template("home.html", all_songs = songs, user = user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/edit/<int:song_id>')
def edit_page(song_id):
    data = {
        'song_id': song_id
    }
    song = Song.get_one_song(data)
    return render_template('edit.html', song = song)

@app.route('/add_song')
def add_song():
    return render_template("add_song.html")

@app.route('/create_song', methods=['POST'])
def create_song():
    if not Song.validate_song(request.form):
        return redirect('/add_song')

    song = Song.create_song(request.form, session['user_id'])
    return redirect('/home')

@app.route('/update_song', methods=['POST'])
def update_song():
    if not Song.validate_song(request.form):
        return redirect('/edit/')
    song = Song.update_song(request.form)
    return redirect("/home")

@app.route('/delete/<int:song_id>')
def delete_song(song_id):
    song = Song.delete_song(song_id)
    return redirect('/home')

@app.route('/show/<int:song_id>')
def get_song_details(song_id):
    song_details = Song.get_song_details(song_id)
    return render_template("song_details.html", **song_details)

@app.route('/like/<int:song_id>')
def like_a_song(song_id):
    user_id = session['user_id']
    like = Song.like_song(user_id, song_id)
    return redirect('/home')


if __name__=="__main__":
    app.run(debug=True, port=5001)