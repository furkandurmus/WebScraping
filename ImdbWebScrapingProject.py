# -*- coding: utf-8 -*-
"""@author: furkan
"""



from requests import get
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import pandas as pd

# this is the url that we wanna dig in
url = 'https://www.imdb.com/search/title/?release_date=2019-01-01,2019-12-31'


response = get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')


movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')


first = movie_containers[0]

print("First Films Name:", first.h3.a.get_text())
print("First Films Rating:", first.find('div', class_="inline-block ratings-imdb-rating").get_text().replace('\n',''))

#get the name of the films, ratings, metascore, votings and release year. 
#Metascore parameter is not valid for all the data so we needed to check 
#if it is null or not in a for loop.
films = [i.h3.a.get_text() for i in movie_containers]
ratings = [i.find('strong').get_text() for i in movie_containers]
metascore = []
for i in movie_containers:
    if i.find('span', class_="metascore") == None:
        metascore.append(None)
    else:
        metascore.append(i.find('span', class_="metascore").get_text())

# [i.find('span', class_="metascore favorable").get_text() for i in movie_containers if i.find('span', class_="metascore favorable") is None i=None]
release_year = [i.find('span', class_="lister-item-year text-muted unbold").get_text() for i in movie_containers]
votings=[i.find('span', attrs = {'name':'nv'}).text for i in movie_containers]

# from the collected data we created a simple data frame object.
data = pd.DataFrame({"Film Name":films, "Votes":votings, "Ratings":ratings, "Metascore":metascore, "Release Year":release_year})

# we extracted the integers only by regex
data["Ratings"]=data["Ratings"].str.extract("(\d+\.\d+)")



