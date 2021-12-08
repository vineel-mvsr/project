from flask import Flask, request, render_template, redirect, url_for
import json
from werkzeug.wrappers import response
app = Flask(__name__)

songs = []

with open('data/songData.json') as f:
    data = json.loads(f.read())
    songs = data['songs']


def removeInvalidDates():
    songsList = songs[:]
    datesList = []

    for song in songsList:
        if song['songReleaseDate'] is not None:
            date = song['songReleaseDate'].split('/')
            if date[0] is None or date[1] is None or date[2] is None:
                datesList.append(song['songReleaseDate'])
            else:
                mon = int(date[0])
                day = int(date[1])
                year = int(date[2])
                if day <= 0 or mon <= 0 or year <= 0:
                    datesList.append(song['songReleaseDate'])
                elif day > 31 or mon > 12 or year < 1500:
                    datesList.append(song['songReleaseDate'])
                elif day > 0 and mon > 0 and year > 0:
                    if mon == 2:
                        if year % 4 == 0 and day > 29:
                            datesList.append(song['songReleaseDate'])
                        elif year % 4 != 0 and day > 28:
                            datesList.append(song['songReleaseDate'])
                elif mon == 1 or mon == 3 or mon == 5 or mon == 7 or mon == 8 or mon == 10 or mon == 12:
                    if day > 31:
                        datesList.append(song['songReleaseDate'])
                elif mon == 4 or mon == 6 or mon == 9 or mon == 11:
                    if day > 30:
                        datesList.append(song['songReleaseDate'])

    for date in datesList:
        for song in songsList:
            if date == song['songReleaseDate']:
                songsList.remove(song)

    return songsList


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'].strip() != 'admin' or request.form['password'] != 'test123':
            error = 'Invalid Credentials....Please do try again....'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route("/home", methods=["GET"])
def home():
    songsList = removeInvalidDates()

    if len(songsList) > 0:
        return render_template('index.html', response=songsList)
    else:
        return render_template("error.html")


@app.route("/sort/", methods=["GET"])
def sort():
    key = request.values['key']
    if key is None:
        return render_template("error.html")

    order = 'asc'
    reverse = True
    if 'order' in request.values:
        order = request.values['order']
    if order == 'asc':
        reverse = False

    if order is None:
        return render_template("error.html")

    sortedList = removeInvalidDates()

    if len(sortedList) <= 0:
        return render_template("error.html")

    sortedList.sort(key=lambda x: x[key], reverse=reverse)

    if len(sortedList) > 0:
        return render_template("index.html", response=sortedList, sort_key=key, sort_order=order)
    else:
        return render_template("error.html")


@app.route("/search/", methods=["GET"])
def searchSongArtist():
    artistList = []
    name = request.values['q']

    if name is None:
        return render_template("error.html")
    songsList = removeInvalidDates()

    if len(songsList) <= 0:
        return render_template("error.html")

    artistList = [song for song in songsList if name.lower(
    ).strip() in song['artist'].lower().strip() or name.lower().strip() in song['song'].lower()]

    if(len(artistList) > 0):
        return render_template("index.html", response=artistList, searchQuery=name)
    else:
        return render_template('error.html', name=name)


if __name__ == "__main__":
    app.run(debug=True)
