import csv
import random
import tkinter as tk
from tkinter import filedialog

# List of possible genres
genres = [
    "Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance", 
    "Thriller", "Animation", "Documentary", "Fantasy", "Mystery", "Western",
    "Musical", "Crime", "War", "Superhero", "Historical", "Adventure", "Family"
]

base_titles = [
    "The Great Adventure", "Love in the City", "Mystery of the Lost", "Space Odyssey", 
    "Haunted House", "Comedy Night", "Drama Unfolds", "Action Hero", 
    "Sci-Fi Future", "Romantic Getaway", "The Last Stand", "Shadow of Fear",
    "Whispers in the Dark", "Echoes of Time", "Rise of the Phoenix", "Silent Guardian",
    "Undercover Mission", "The Forgotten Realm", "Beyond the Stars", "Twilight Chronicles",
    "Neon Dreams", "The Lone Ranger", "Haunted Manor", "Cybernetic Dawn", "Parallel Worlds",
    "Fallen Kingdom", "Crimson Horizon", "The Midnight Heist", "Frostbound", "Echoes of War",
    "The Golden Curse", "Vortex of Destiny", "City of Shadows", "Legends Reborn",
    "The Secret Society", "Dark Waters", "Infinite Possibilities", "Beneath the Surface",
    "Storm Chasers", "The Quantum Paradox", "Ghosts of Yesterday", "The Last Lighthouse"
]

# Function to generate a random movie title
def generate_title(index):  
    return f"{base_titles[index % len(base_titles)]} {index + 1}"

# Generate 50 movie entries
def generate_movies():
    movies = []
    for i in range(50):
        title = generate_title(i)
        genre = random.choice(genres)
        release_year = random.randint(1980, 2025)
        rating = round(random.uniform(0.0, 10.0), 1)
        votes = random.randint(100, 10000)
        movies.append([title, genre, release_year, rating, votes])
    return movies

# Function to save CSV with file dialog
def save_csv_with_dialog():
    # Initialize Tkinter root (hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Open file save dialog
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Save Movies CSV",
        initialfile="movies.csv"
    )

    # If a file path was selected, write the CSV
    if file_path:
        movies = generate_movies()
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["title", "genre", "release_year", "rating", "votes"])
            writer.writerows(movies)
        print(f"CSV file saved successfully at: {file_path}")
    else:
        print("File save canceled by user.")

# Run the save function
if __name__ == "__main__":
    save_csv_with_dialog()