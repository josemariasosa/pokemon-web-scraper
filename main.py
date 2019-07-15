#!/usr/bin/env python
# coding=utf-8

# ------------------------------------------------------------------------------
# Processing Pokemon data
# ------------------------------------------------------------------------------
# jose maria sosa

import pandas as pd
pd.set_option('display.max_columns', 20)

# import re
import bs4 as bs
import requests

# import os

# from pathlib import Path


# import re
# import requests

# import bs4 as bs
# import pandas as pd


# class PokemonWebScraper(object):

#     img_url = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/{}.png"
#     poke_domain = "https://www.pokemon.com"
#     csv_file = "./files/pokedex.csv"
#     sheet_name = "full"
#     table_name = "pokedex"

#     """ Simple exercise to:
#             - Parse a HTML file using beautifulsoup.
#             - Download images from url to local.
#             - Update into a Google Spread Sheet.
#     """

#     def downloadPokedex(self):

#         url = self.poke_domain + "/us/pokedex/"

#         # 1. Get the HTML Source File.
#         print(url)
#         r = requests.get(url)
#         print(r); exit()
#         soup = bs.BeautifulSoup(r.content, 'lxml')

#         # 2. Extract the data and append it to a list.
#         pokedex = []
#         for sec in soup.find_all('li'):
#             for link in sec.find_all('a'):
#                 if 'href' in link.attrs.keys():
#                     if re.search(r'/pokedex/(.+)', link['href']):
#                         pokemon = link.text
#                         pokemon = pokemon.split(' - ')
#                         pokemon = [x.strip() for x in pokemon]
#                         pokedex.append({
#                             'name': pokemon[1].lower(),
#                             'number': int(pokemon[0]),
#                             'ref': link['href']
#                         })

#         # 3. Generate a dataframe.
#         pokedex = pd.DataFrame(pokedex)[['number', 'name', 'ref']].copy()

#         # 4. Download the file as csv.
#         pokedex.to_csv(self.csv_file, index=False)

#     # --------------------------------------------------------------------------
    
#     def insertTypes(self, pokedex):

#         aug_pokedex = []
#         for index, row in pokedex.head(10).iterrows():

#             # 1. Get the HTML file from each pokemon.
#             poke_url = self.poke_domain + row['ref']
#             r = requests.get(poke_url)
#             soup = bs.BeautifulSoup(r.content, 'lxml')

#             # 2. Append the types to the list.
#             type_list = []
#             for section in soup.find_all('ul'):
#                 for link in section.find_all('a'):
#                     if link['href'] == row['ref']:
#                         for _type in link.find_all('li'):
#                             type_list.append(_type.text.lower())

#             old_img_name = "{0:0=3d}".format(int(row['number']))
#             from_url = self.img_url.format(old_img_name)

#             to_location = "./images/ok/{}/{}.png"
#             new_img_name = "{}-{}".format(old_img_name, row['name'])
#             to_location = to_location.format(type_list[0], new_img_name)

#             aug_pokedex.append({
#                 'name': row['name'],
#                 'number': row['number'],
#                 'ref': row['ref'],
#                 'type': type_list,
#                 'from_url': from_url,
#                 'to_location': to_location
#             })

#         aug_pokedex = pd.DataFrame(aug_pokedex)

#         return aug_pokedex

#     # --------------------------------------------------------------------------
    
#     def setDirStructure(self, pokedex):

#         """ Only the first type will be considered for a directory.
#         """

#         if not os.path.isdir('./images/'):
#             os.mkdir('./images/')

#         if not os.path.isdir('./images/ok/'):
#             os.mkdir('./images/ok/')

#         types_list = pokedex['type'].tolist()
#         all_types = list(set([x[0] for x in types_list]))

#         for _type in all_types:
#             directory = './images/ok/{}'.format(_type)
#             if not os.path.isdir(directory):
#                 os.mkdir(directory.format(_type))

#         return None

#     # --------------------------------------------------------------------------
    
#     def downloadAllImages(self, pokedex):

#         for index, row in pokedex.iterrows():

#             from_location = row['from_url']
#             to_location = row['to_location']

#             if not os.path.exists(to_location):
#                 response = requests.get(from_location)
#                 if response.status_code == 200:
#                     with open(to_location, 'wb') as f:
#                         f.write(response.content)

#         return None

#     # --------------------------------------------------------------------------
# # ------------------------------------------------------------------------------

# def main():

#     pk = PokemonWebScraper()

#     # 1. Generate a csv file with the name and number of all Pokemons.
#     pk.downloadPokedex()

#     # 2. After manually upload the table to Google Sheets, import it.
#     pokedex = pd.read_csv('files/pokedex.csv')

#     # 3. For each pokemon url, get the pokemon types.
#     pokedex = pk.insertTypes(pokedex)

#     # 4. Generate the directories structure.
#     pk.setDirStructure(pokedex)

#     # 5.pk Download all the images into the directories.
#     pk.downloadAllImages(pokedex)

#     # 6. Export the file locally and in Google Drive.
#     pokedex['type'] = pokedex['type'].map(lambda x: '-'.join(x))

#     select = ['number', 'name', 'ref', 'to_location', 'type']
#     pokedex = pokedex[select].copy()

#     pokedex.to_csv('files/results.csv', index=False)

#     print (pokedex)

# # ------------------------------------------------------------------------------

# if __name__ == '__main__':
#     main()
