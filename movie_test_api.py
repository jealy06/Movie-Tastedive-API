from webbrowser import get
import requests
import json
import cache

api_key = '432980-Test-ECLNUC8B'

base_url = 'https://tastedive.com/api/similar'

def get_movies_from_tastedive(movie='Black Panther',movie_limit='5'):
    res = {}
    taste = {}
    taste['q'] = movie
    taste['limit'] = movie_limit
    taste['type'] = 'movies'
    taste['k'] = api_key

    resp = requests.get(base_url,params=taste)
    #print(resp.text)
    #print(type(resp))
    #print(resp.url)
    resp_py = resp.json()
    return resp_py

#print(get_movies_from_tastedive())

def extract_movie_titles(mov_dict = {}):
    mov_dict = mov_dict['Similar']['Results']
    movies_list = []
    for name in mov_dict:
        movies_list.append(name['Name'])

    return movies_list #returns a list of 5 movie names

#print(extract_movie_titles(get_movies_from_tastedive()))

def get_related_titles(movie_list = []):
    
    new = []  
    twentyfive_movies = []
    for movie in movie_list:
        mov_json = get_movies_from_tastedive(movie) 
        new.append(extract_movie_titles(mov_json))
    for item in new:
        for movie in item:
            if movie not in twentyfive_movies:
                twentyfive_movies.append(movie)

    return twentyfive_movies #returns list of up to 25 movies

#print(get_related_titles())

movie_title = ''
omdb_apikey = '493ac6a7'
omdb_url = 'http://www.omdbapi.com/'

def get_movie_data(movie_title=''):
    omdb_dict = {}
    omdb_dict['apikey'] = omdb_apikey
    omdb_dict['t'] = movie_title
    omdb_dict['r'] = 'json'
    try:
        omdb_resp = requests.get(omdb_url,params=omdb_dict)
        #print(omdb_resp.text)
        #print(omdb_resp.url)
        omdb_resp_py = omdb_resp.json()
        #print(json.dumps(omdb_resp_py,indent=3))
        return omdb_resp_py
    except:
        return 0
#print(get_movie_data('Avatar'))

def get_movie_rating(movie_data = {}):
    
    try:
        ratings = movie_data['Ratings']

        for rotten in ratings:

            if rotten['Source'] == 'Rotten Tomatoes':
                rot_val = rotten['Value']
                rot_val = rot_val.strip('%')
                return int(rot_val)
        return 0
    except:
        print('Bad Data')
        return 0


five_movies = get_movies_from_tastedive('Spawn') #gives you 5 movies
movie_titles = extract_movie_titles(five_movies) #extracts titles
twofive_listmovies = get_related_titles(movie_titles)

#get_sorted_recommendations
#define your list of movies

def sorting_movies(movies = {}): #takes in a dictionary 
    return (movies[1],movies[0]) #returns a tuple of movie integer and movie

# def get_sorted_recommendations():
#     final = {}

#     for movie in twofive_listmovies: #iterate through list of 25 movies
#         movie_data = get_movie_data(movie) #pull movie data
#         movie_rating = get_movie_rating(movie_data) #get movie rating from data
#         if movie not in final:
#             final[movie] = movie_rating #append the rating and movie to a dictionary
#     #sorting_vals = sorting_movies(final)
#     return sorted(final.items(),key=sorting_movies,reverse=True)

def get_sorted_recommendations(listmovie = []):
    final = {}
    x = {}
    y = []
    count = 0
    for movie in listmovie:
        five_movies = get_movies_from_tastedive(movie)
        movie_titles = extract_movie_titles(five_movies)
        twofive_listmovies = get_related_titles(movie_titles)
        for m_2 in twofive_listmovies: #iterate through list of 25 movies
            movie_data = get_movie_data(m_2) #pull movie data
            movie_rating = get_movie_rating(movie_data) #get movie rating from data
            if m_2 not in final:
                final[m_2] = movie_rating #append the rating and movie to a dictionary
        #sorting_vals = sorting_movies(final)
        #print(final,movie)
        y = sorted(final.items(),key=sorting_movies,reverse=True)[:5]
        if movie not in x:
            x[movie] = y

        final = {}
    #print(final, len(final))
    #print(final.items())
    
    return x
        
def get_sorting_recommendations(lst):
    x=get_related_titles(lst)
    x.sort()
    rate_lst=[]
    for i in range(len(x)):
        rate_lst.append(get_movie_rating(get_movie_data(x[i])))
    sorted_lst=[]
    #rate_lst.sort()
    dd=dict((i, rate_lst.count(i)) for i in rate_lst)
    #print(dd)
    final=list(zip(x,rate_lst)) 
    y=sorted(final,key=sorting_movies,reverse=True)
    for movie in y:
        sorted_lst.append(movie[0])
    return sorted_lst      
print(get_sorting_recommendations(["Bridesmaids", "Sherlock Holmes"]))

#print(get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"]))
#print(get_sorted_recommendations(['Hangover', 'Dear John']))