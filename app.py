from flask import Flask, render_template, request, url_for, redirect, abort
import sqlite3 as sql


app = Flask(__name__)

api_key=""
base_url="https://api.tmdb.org/3/discover/movie/?api_key="+api_key

# filmflixDB connection 
def filmflix():
    conn = sql.connect('filmflix.db')
    conn.row_factory = sql.Row
    return conn

"home route"
@app.route('/') # set up home route/link to the home page

@app.route('/home')

def home():
    import json
    import urllib.request as request
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    conn = request.urlopen(base_url)
    json_data = json.loads(conn.read())
    print(json_data)
    print(base_url)

    return render_template('home.html', data=json_data["results"],title = 'Home')

@app.route('/addfilms', methods=['GET', 'POST'])
def addfilms():
    if request.method == 'POST':
        title = request.form['title']
        yearreleased = request.form['yearreleased']
        rating = request.form['rating']
        duration = request.form['duration']
        genre = request.form['genre']

        conn = filmflix()
        cursor = conn.cursor()
        filmID = cursor.lastrowid
        
        cursor.execute('INSERT INTO tblFilms (filmID, title, yearreleased, rating, duration, genre) VALUES (?,?,?,?,?,?)',(filmID, title, yearreleased, rating, duration, genre))
        conn.commit()
        conn.close()
        return redirect(url_for('films'))
    return render_template('addfilms.html', title = 'Add Films')

@app.route('/films')
def films():
    conn = filmflix()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tblFilms")
    getFilms = cursor.fetchall()

    return render_template('films.html', title = 'Films', retrieveFilms = getFilms)
def getFilmID(filmID):
    conn = filmflix()
    cursor = conn.cursor()
    film = cursor.execute("SELECT * FROM tblFilms WHERE filmID  = ?", (filmID,)).fetchone()
    conn.close()
    if film is None:
        abort(404)
    return film

"use the route /<int:id>/update" # filmID is a placeholder
@app.route('/<int:filmID>/update', methods =['GET', 'POST'])

def update(filmID): # passed in the primary key filmID from the song Table
    filmRecord = getFilmID(filmID)
    if request.method == 'POST':
        title = request.form['title']
        yearreleased = request.form['yearreleased']
        rating = request.form['rating']
        duration = request.form['duration']
        genre = request.form['genre']

        conn = filmflix()
        cursor = conn.cursor()
        cursor.execute('UPDATE tblFilms SET title =?, yearreleased =?, rating=?, duration=?, genre=? WHERE filmID=?', ( title, yearreleased, rating, duration, genre, filmID,))
        conn.commit()
        conn.close()
        return redirect(url_for('films'))

    return render_template('update.html',title= 'Update Films' , filmRecord = filmRecord)


@app.route('/<int:filmID>/delete', methods= ('POST',))
def delete(filmID):
    conn = filmflix()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tblFilms WHERE filmID = ?",(filmID,))
    conn.commit()
    conn.close()
    return redirect(url_for('films'))


if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0', port=8124)
