from flask import Blueprint, abort, redirect, render_template, request, url_for

from app.db import get_db

bp = Blueprint('movies', __name__, url_prefix='/movies')

@bp.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM movies')
    movies = cursor.fetchall()
    return render_template('movies/index.html', movies=movies)

def get_movie(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM movies WHERE id = %s', (id,))
    movie = cursor.fetchone()
    return movie

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        genre= request.form['genre']
        release_date = request.form['release_date']
        cast = request.form['cast']
        director = request.form['director']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO movies (title, description, genre, release_date, cast, director) VALUES (%s, %s, %s, %s, %s, %s)', (title, description, genre, release_date, cast, director))
        db.commit()
        return redirect(url_for('movies.index'))

    return render_template('movies/create.html')

@bp.route('/<int:id>')
def show(id):
    movie = get_movie(id)

    if movie is None:
        # redirect to not found page
        abort(404)
    return render_template('movies/show.html', movie=movie)

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        genre= request.form['genre']
        release_date = request.form['release_date']
        cast = request.form['cast']
        director = request.form['director']
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE movies SET title = %s, description = %s, genre = %s, release_date = %s, cast = %s, director = %s WHERE id = %s', (title, description, genre, release_date, cast, director, id))
        db.commit()
        return redirect(url_for('movies.index'))

    movie = get_movie(id)
    return render_template('movies/edit.html', movie=movie)