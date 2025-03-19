from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib
from peewee import *
from sklearn.linear_model import LinearRegression
from plots import plot_avg_rating_per_year, plot_movies_per_genre, plot_rating_by_genre_box, plot_rating_distribution, plot_rating_vs_votes

app = Flask(__name__)
matplotlib.use('Agg')

# Database setup with SQLite and Peewee ORM
db = SqliteDatabase('movies.db')

class Movie(Model):
    title = CharField()
    genre = CharField()
    release_year = IntegerField()
    rating = FloatField()
    votes = IntegerField()

    class Meta:
        database = db

# Initialize database
db.connect()
if bool(Movie.select()):
    Movie.delete().execute()  # Clear existing data for simplicity
db.create_tables([Movie], safe=True)

# Load CSV data into the database
def load_csv_to_db(csv_file):
    df = pd.read_csv(csv_file)
    Movie.delete().execute()  # Clear existing data for simplicity
    for _, row in df.iterrows():
        Movie.create(
            title=row['title'],
            genre=row['genre'],
            release_year=row['release_year'],
            rating=row['rating'],
            votes=row['votes']
        )

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            load_csv_to_db(file)
            return redirect(url_for('visualizations'))
    return render_template('upload.html')

@app.route('/visualizations', methods=['GET', 'POST'])
def visualizations():
    movies = Movie.select()
    no_data = not bool(movies)
    if no_data:
        return render_template('visualizations.html', no_data=no_data)

    # Define available plot options
    plot_options = [
        {"id": "genre", "title": "Filmas pēc žanra", "func": plot_movies_per_genre},
        {"id": "year", "title": "Vidējais vērtējums gadā", "func": plot_avg_rating_per_year},
        {"id": "votes", "title": "Vērtējums vs. Balss", "func": plot_rating_vs_votes},
        {"id": "distribution", "title": "Vērtējumu izplatīšana", "func": plot_rating_distribution},
        {"id": "box", "title": "Vērtējumu izplatīšana pēc žanra", "func": plot_rating_by_genre_box}
    ]

    df = pd.DataFrame(list(movies.dicts()))
    selected_plot = None

    if request.method == 'POST':
        selected_id = request.form.get('plot_type')
        for plot in plot_options:
            if plot["id"] == selected_id:
                selected_plot = (plot["title"], plot["func"](df))
                break
    else:
        # Default to first plot on initial load if GET
        selected_plot = (plot_options[0]["title"], plot_options[0]["func"](df))

    return render_template('visualizations.html', no_data=no_data, plot_options=plot_options, selected_plot=selected_plot)

@app.route('/database')
def database():
    movies = Movie.select()
    no_data = not bool(movies)
    return render_template('database.html', no_data=no_data, movies=movies)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    movies = Movie.select()
    no_data = not bool(movies)
    if no_data:
        return render_template('predict.html', no_data=no_data)
    if request.method == 'POST':
        df = pd.DataFrame(list(movies.dicts()))
        x = df[['votes']]
        y = df['rating']
        model = LinearRegression()
        model.fit(x, y)
        votes = int(request.form['votes'])
        predicted_rating = model.predict([[votes]])[0]
        return render_template('predict.html', no_data=no_data, prediction=f"{predicted_rating:.2f}")
    return render_template('predict.html', no_data=no_data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)