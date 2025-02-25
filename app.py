from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from peewee import *
from sklearn.linear_model import LinearRegression
from io import BytesIO
import base64

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

# Plot functions returning base64-encoded images
def plot_movies_per_genre(df):
    plt.figure(figsize=(10, 6))
    genre_count = df['genre'].value_counts()
    sns.barplot(x=genre_count.index, y=genre_count.values)
    plt.xlabel('Genre')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.clf()
    plt.close('all')
    return plot_data

def plot_avg_rating_per_year(df):
    plt.figure(figsize=(10, 6))
    yearly_rating = df.groupby('release_year')['rating'].mean()
    yearly_rating.plot(kind='line')
    plt.xlabel('Release Year')
    plt.ylabel('Average Rating')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.clf()
    plt.close('all')
    return plot_data

def plot_rating_vs_votes(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='votes', y='rating', data=df)
    plt.xlabel('Votes')
    plt.ylabel('Rating')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.clf()
    plt.close('all')
    return plot_data

def plot_rating_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['rating'], bins=20, kde=True)
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.clf()
    plt.close('all')
    return plot_data

def plot_rating_by_genre_box(df):
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='genre', y='rating', data=df)
    plt.xlabel('Genre')
    plt.ylabel('Rating')
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()
    return plot_data

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
        {"id": "genre", "title": "Movies per Genre", "func": plot_movies_per_genre},
        {"id": "year", "title": "Average Rating per Year", "func": plot_avg_rating_per_year},
        {"id": "votes", "title": "Rating vs. Votes", "func": plot_rating_vs_votes},
        {"id": "distribution", "title": "Distribution of Ratings", "func": plot_rating_distribution},
        {"id": "box", "title": "Rating Distribution by Genre", "func": plot_rating_by_genre_box}
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
        X = df[['votes']]
        y = df['rating']
        model = LinearRegression()
        model.fit(X, y)
        votes = int(request.form['votes'])
        print(model.predict([[votes]]))
        predicted_rating = model.predict([[votes]])[0]
        return render_template('predict.html', no_data=no_data, prediction=f"{predicted_rating:.2f}")
    return render_template('predict.html', no_data=no_data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)