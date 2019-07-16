#!/usr/bin/env python
# coding=utf-8

# ------------------------------------------------------------------------------
# Pokemon Web Scraper | Exercise 1
# ------------------------------------------------------------------------------
# jose maria sosa

import os
import re
import requests

import bs4 as bs
import pandas as pd
pd.set_option('display.max_columns', 20)


# ------------------------------------------------------------------------------
# 1. Get a file with all the pokemons.

def generatePokemonCsv():

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
    pokedex.to_csv('files/pokedex.csv', index=False)


# ------------------------------------------------------------------------------
# 2. Using only the first 15 Pokemons, extract the pokemon types.

def getPokemonType():

    pok_url = "https://www.pokemon.com"
    img_url = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/{}.png"

    pokedex = pd.read_csv('files/pokedex.csv').head(15)

    pokemon_type = []
    for index, row in pokedex.iterrows():

        # 1. Get the HTML file from each pokemon.
        full_pok_url = pok_url + row['ref']
        r = requests.get(full_pok_url)
        soup = bs.BeautifulSoup(r.content, 'lxml')

        # 2. Append the types to the list.
        type_list = []
        for section in soup.find_all('ul'):
            for link in section.find_all('a'):
                if link['href'] == row['ref']:
                    for _type in link.find_all('li'):
                        type_list.append(_type.text.lower())

        type_str = '-'.join(type_list)

        # 3. Generate the image url.
        old_img_name = "{0:0=3d}".format(int(row['number']))
        full_img_url = img_url.format(old_img_name)

        pokemon_type.append({
            'name': row['name'],
            'number': row['number'],
            'ref': row['ref'],
            'type': type_str,
            'img_url': full_img_url
        })

    pokemon_type = pd.DataFrame(pokemon_type)
    pokemon_type.to_csv('files/pokedex_types.csv', index=False)


# ------------------------------------------------------------------------------
# 3. Using only the 1st type for each Pokemon, generate the following 
# file structure, and download the Pokemon image in a local location.

def setDirs(pokedex):

    if not os.path.isdir('./images/'):
        os.mkdir('./images/')

    if not os.path.isdir('./images/ok/'):
        os.mkdir('./images/ok/')

    types_list = pokedex['type'].tolist()
    all_types = list(set([x.split('-')[0] for x in types_list]))

    for _type in all_types:
        directory = './images/ok/{}'.format(_type)
        if not os.path.isdir(directory):
            os.mkdir(directory.format(_type))

def downloadImages(pokedex):

    for index, row in pokedex.iterrows():

        from_location = row['img_url']

        poke_num = "{0:0=3d}".format(int(row['number']))
        poke_type = row['type'].split('-')[0]
        img_name = "{}-{}".format(poke_num, row['name'])

        to_location = "./images/ok/{}/{}.png"
        to_location = to_location.format(poke_type, img_name)

        if not os.path.exists(to_location):
            response = requests.get(from_location)
            if response.status_code == 200:
                with open(to_location, 'wb') as f:
                    f.write(response.content)


# ------------------------------------------------------------------------------
# 

def main():

    # 1. Generating csv-file with all the pokemons.
    generatePokemonCsv()

    # 2. Get the pokemon types for the first 14 pokemons.
    getPokemonType()

    # 3. Get the pokemon images.
    pokedex = pd.read_csv('files/pokedex_types.csv')

    setDirs(pokedex)
    downloadImages(pokedex)

# ------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
