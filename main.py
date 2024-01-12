# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 17:54:20 2023

@author: ars16
"""

import requests
import csv
import config


# TMDb API URL
api_url = "https://api.themoviedb.org/3/discover/movie"

api_key=config.api_key

# Number of movies to retrieve
num_movies = 50

# Parameters for the TMDb API request
params = {
    'api_key': api_key,
    'language': 'en-US',
    'sort_by': 'popularity.desc',
    'include_adult': 'false',
    'include_video': 'false',
    'page': 1  # Start with page 1
}

# List to store movie data
movies_data = []

# Retrieve movie data from TMDb
for page in range(1, (num_movies // 20) + 1):
    params['page'] = page
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        movie_data = response.json().get('results')
        movies_data.extend(movie_data)

# Define the CSV file name
csv_file = 'tmdb_movies.csv'

# Write movie data to a CSV file
with open(csv_file, mode='w', newline='',encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['Title', 'Release Date', 'Overview', 'Popularity', 'Vote Average', 'Vote Count', 'Keywords', 'Runtime', 'Cast', 'Director', 'Editor', 'Poster URL'])
    # Write movie data to the CSV file
    for movie in movies_data:
        # Retrieve additional details for each movie
        movie_details_url = f"https://api.themoviedb.org/3/movie/{movie['id']}"
        details_response = requests.get(movie_details_url, params={'api_key': api_key, 'append_to_response': 'credits,keywords'})
        details = details_response.json()
    
        # Extract keywords
        keywords = ', '.join(keyword['name'] for keyword in details.get('keywords', {}).get('keywords', []))
    
        # Extract runtime (in minutes)
        runtime = details.get('runtime', 'N/A')
    
        # Extract cast members
        cast = ', '.join(member['name'] for member in details.get('credits', {}).get('cast', []))
    
        # Retrieve full crew list for each movie
        crew_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/credits"
        crew_response = requests.get(crew_url, params={'api_key': api_key})
        crew = crew_response.json().get('crew', [])
    
        # Extract director(s)
        directors = ', '.join(member['name'] for member in crew if member['job'] == 'Director')
    
        # Extract editor(s)
        editors = ', '.join(member['name'] for member in crew if member['job'] == 'Editor')

        # Extract poster URL
        poster_url = f"https://image.tmdb.org/t/p/original/{details.get('poster_path')}" if details.get('poster_path') else 'N/A'

        # Write all data to the CSV
        writer.writerow([movie['title'], movie['release_date'], movie['overview'], movie['popularity'], movie['vote_average'], movie['vote_count'], keywords, runtime, cast, directors, editors, poster_url])

print(f'{len(movies_data)} movies data saved to {csv_file}2')

