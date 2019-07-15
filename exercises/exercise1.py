#!/usr/bin/env python
# coding=utf-8

# ------------------------------------------------------------------------------
# Pokemon Web Scraper | Exercise 1
# ------------------------------------------------------------------------------
# jose maria sosa

import re
import requests

import bs4 as bs
import pandas as pd
pd.set_option('display.max_columns', 20)


# ------------------------------------------------------------------------------
# 1. Get a file with all the pokemons.

# 1. Get the HTML Source File.
url = "https://www.pokemon.com/us/pokedex/"
r = requests.get(url)
soup = bs.BeautifulSoup(r.content, 'lxml')

# 2. Extract the data and append it to a list.
pokedex = []
for sec in soup.find_all('li'):
    for link in sec.find_all('a'):
        if 'href' in link.attrs.keys():
            if re.search(r'/pokedex/(.+)', link['href']):
                pokemon = link.text
                pokemon = pokemon.split(' - ')
                pokemon = [x.strip() for x in pokemon]
                pokedex.append({
                    'name': pokemon[1].lower(),
                    'number': int(pokemon[0]),
                    'ref': link['href']
                })

# 3. Generate a dataframe.
pokedex = pd.DataFrame(pokedex)[['number', 'name', 'ref']].copy()

# 4. Download the file as csv.
print(pokedex)




# ------------------------------------------------------------------------------
# 1. Print the Total_Orders.

###############################
### Code the solution here! ###
###############################

# ------------------------------------------------------------------------------
# 2. Print the sales and orders only of May 2019.

###############################
### Code the solution here! ###
###############################


# ------------------------------------------------------------------------------
# 3. Print the table of sales as a Pandas DataFrame.

###############################
### Code the solution here! ###
###############################


# ------------------------------------------------------------------------------
# 4. Calculate the Forecast for september using the average of the last 3 month.

###############################
### Code the solution here! ###
###############################


# ------------------------------------------------------------------------------
# 5. Calculate the Average Ticket Price.

###############################
### Code the solution here! ###
###############################

