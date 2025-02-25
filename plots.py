import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

matplotlib.use('Agg')

# Plot functions returning base64-encoded images
def plot_movies_per_genre(df):
    plt.figure(figsize=(10, 6))
    genre_count = df['genre'].value_counts()
    sns.barplot(x=genre_count.index, y=genre_count.values)
    plt.xlabel('Žanrs')
    plt.ylabel('Daudzums')
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
    plt.xlabel('Izdošanas gads')
    plt.ylabel('Vidējais vērtējums')
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
    plt.xlabel('Balsis')
    plt.ylabel('Vērtējums')
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
    plt.xlabel('Vērtējums')
    plt.ylabel('Biežums')
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
    plt.xlabel('Žanrs')
    plt.ylabel('Vērtējums')
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()
    return plot_data